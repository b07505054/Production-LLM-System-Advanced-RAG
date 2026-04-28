from app.schemas.query import ChunkResult


class GroundedAnswerGenerator:
    """
    Thin generation layer.

    For now, this is a deterministic local generator.
    Later it can be replaced with OpenAI / Anthropic / local LLM.
    """

    def generate(self, query: str, context_chunks: list[ChunkResult]) -> str:
        if not context_chunks:
            return "I could not find enough relevant evidence to answer the question."

        evidence = "\n".join(
            f"[{idx + 1}] {chunk.text}"
            for idx, chunk in enumerate(context_chunks[:3])
        )

        return (
            f"Question: {query}\n\n"
            f"Grounded answer:\n"
            f"Based on the retrieved evidence, the most relevant answer is supported by the following context:\n\n"
            f"{evidence}\n\n"
            f"In short, the answer should be based only on the retrieved chunks above."
        )


answer_generator = GroundedAnswerGenerator()