__all__ = [
    # llm
    "classifier",
    "coder",
    "extractor",
    "function",
    "generator",
    "validator",
    "patch",
    "planner",
    "prompter",
    "qa",
    "solver",
    "query",

    # nlp/data
    "chunker",
    "reader",

    # multimodal
    "image",
    "audio",
    "transcribe"
]


from .._utils.helpers import router


class classifier(router):
    pass


classifier.init("xnano.resources.classify", "classifier")


class coder(router):
    pass

coder.init("xnano.resources.code", "coder")


class extractor(router):
    pass

extractor.init("xnano.resources.extract", "extractor")


class function(router):
    pass


function.init("xnano.resources.function_constructor", "function")


class generator(router):
    pass

generator.init("xnano.resources.generate", "generator")


class validator(router):
    pass


validator.init("xnano.resources.validate", "validator")


class patch(router):
    pass

patch.init("xnano.resources.patch", "patch")


class planner(router):
    pass


planner.init("xnano.resources.plan", "planner")


class prompter(router):
    pass


prompter.init("xnano.resources.prompt", "prompter")


class qa(router):
    pass

qa.init("xnano.resources.question_answer", "qa")


class solver(router):
    pass


solver.init("xnano.resources.solve", "solver")


class query(router):
    pass


query.init("xnano.resources.query", "query")


class chunker(router):
    pass


chunker.init("xnano.resources.chunk", "chunker")


class reader(router):
    pass


reader.init("xnano.resources.read", "reader")


class image(router):
    pass


image.init("xnano.resources.multimodal", "image")


class audio(router):
    pass


audio.init("xnano.resources.multimodal", "audio")


class transcribe(router):
    pass


transcribe.init("xnano.resources.multimodal", "transcribe")







