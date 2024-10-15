from __future__ import annotations

import logging
import typing as t
from dataclasses import dataclass, field

import numpy as np

from ragas.dataset_schema import SingleTurnSample
from ragas.metrics._faithfulness import (
    FaithfulnessStatements,
    HasSegmentMethod,
    LongFormAnswerPrompt,
    NLIStatementInput,
    NLIStatementPrompt,
)
from ragas.metrics.base import (
    MetricType,
    MetricWithLLM,
    SingleTurnMetric,
    get_segmenter,
)
from ragas.prompt import PydanticPrompt

if t.TYPE_CHECKING:
    from langchain_core.callbacks import Callbacks


logger = logging.getLogger(__name__)


@dataclass
class NoiseSensitivity(MetricWithLLM, SingleTurnMetric):
    name: str = "noise_sensitivity"  # type: ignore
    focus: t.Literal["relevant", "irrelevant"] = "relevant"
    _required_columns: t.Dict[MetricType, t.Set[str]] = field(
        default_factory=lambda: {
            MetricType.SINGLE_TURN: {
                "user_input",
                "response",
                "reference",
                "retrieved_contexts",
            }
        }
    )
    nli_statements_message: PydanticPrompt = field(default_factory=NLIStatementPrompt)
    statement_prompt: PydanticPrompt = field(default_factory=LongFormAnswerPrompt)
    sentence_segmenter: t.Optional[HasSegmentMethod] = None
    max_retries: int = 1
    _reproducibility: int = 1

    @property
    def reproducibility(self):
        return self._reproducibility

    @reproducibility.setter
    def reproducibility(self, value):
        if value < 1:
            logger.warning("reproducibility cannot be less than 1, setting to 1")
            value = 1
        elif value % 2 == 0:
            logger.warning(
                "reproducibility level cannot be set to even number, setting to odd"
            )
            value += 1
        self._reproducibility = value

    def __post_init__(self):
        if self.sentence_segmenter is None:
            language = self.nli_statements_message.language
            self.sentence_segmenter = get_segmenter(language=language, clean=False)
        if self.focus not in {"relevant", "irrelevant"}:
            raise ValueError(
                f"Invalid argument passed for 'focus': {self.focus}. Must be 'relevant' or 'irrelevant'."
            )
        self.name = f"{self.name}_{self.focus}"  # type: ignore

    async def _evaluate_statement_faithfulness(
        self, statements: t.List[str], context: str, callbacks: Callbacks
    ) -> t.List[int]:
        assert self.llm is not None, "LLM is not set"

        verdicts = await self.nli_statements_message.generate(
            data=NLIStatementInput(context=context, statements=statements),
            llm=self.llm,
            callbacks=callbacks,
        )

        verdict_list = [
            1 if statement.verdict else 0 for statement in verdicts.statements
        ]
        return verdict_list

    async def _decompose_answer_into_statements(
        self, text: str, question: str, callbacks: Callbacks
    ) -> t.List[str]:
        assert self.llm is not None, "LLM is not set"
        assert self.sentence_segmenter is not None, "sentence_segmenter is not set"

        sentences = self.sentence_segmenter.segment(text)
        sentences_with_index = {
            i: sentence
            for i, sentence in enumerate(sentences)
            if sentence.strip().endswith(".")
        }

        statements_simplified = await self.statement_prompt.generate(
            llm=self.llm,
            data=FaithfulnessStatements(
                question=question, answer=text, sentences=sentences_with_index
            ),
            callbacks=callbacks,
        )

        statements = []
        if statements_simplified is None:
            return statements
        for component in statements_simplified.sentences:
            statements.extend(component.simpler_statements)
        return statements

    def _compute_score(self, answers: t.Dict) -> float:
        # relevant retrievals
        relevant_retrieved = np.max(
            answers["retrieved2ground_truth"], axis=0, keepdims=True
        )
        relevant_faithful = np.max(
            relevant_retrieved & answers["retrieved2answer"], axis=1
        )

        # irrelevant retrievals
        irrelevant_retrieved = ~np.max(
            answers["retrieved2ground_truth"], axis=0, keepdims=True
        )
        irrelevant_faithful = np.max(
            irrelevant_retrieved & answers["retrieved2answer"], axis=1
        )

        # to keep them exclusive
        irrelevant_faithful &= ~relevant_faithful

        incorrect = ~answers["ground_truth2answer"]
        noise_sensitivity_in_relevant = np.mean(relevant_faithful & incorrect)
        noise_sensitivity_in_irrelevant = np.mean(irrelevant_faithful & incorrect)

        if self.focus == "irrelevant":
            return noise_sensitivity_in_irrelevant

        return noise_sensitivity_in_relevant

    async def _single_turn_ascore(
        self, sample: SingleTurnSample, callbacks: Callbacks
    ) -> float:
        row = sample.to_dict()
        return await self._ascore(row, callbacks)

    async def _ascore(self: t.Self, row: t.Dict, callbacks: Callbacks) -> float:
        """
        returns the NLI score for each (q, c, a) pair
        """
        assert self.llm is not None, "LLM is not set"

        gt_statements = await self._decompose_answer_into_statements(
            row["reference"], row["user_input"], callbacks
        )
        ans_statements = await self._decompose_answer_into_statements(
            row["response"], row["user_input"], callbacks
        )
        gt_verdictslist = []
        ans_verdictslist = []

        for ctx in row["retrieved_contexts"]:
            verdicts = await self._evaluate_statement_faithfulness(
                gt_statements, ctx, callbacks
            )
            gt_verdictslist.append(np.array(verdicts))

            verdicts = await self._evaluate_statement_faithfulness(
                ans_statements, ctx, callbacks
            )
            ans_verdictslist.append(np.array(verdicts))

        answers = {}
        answers["retrieved2ground_truth"] = np.array(gt_verdictslist).T
        answers["retrieved2answer"] = np.array(ans_verdictslist).T
        answers["ground_truth2answer"] = np.array(
            await self._evaluate_statement_faithfulness(
                ans_statements, row["reference"], callbacks
            )
        )
        answers["ground_truth2answer"] = np.array([answers["ground_truth2answer"]])
        answers = {k: v.astype(bool) for k, v in answers.items()}
        return self._compute_score(answers)
