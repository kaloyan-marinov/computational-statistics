"""
Recipe for Hacking Statistics: Cross Validation (CV)

CV is a way to determine how well a model is fitting data when you don't have
some a-priori description of the data:

- Statisticians have worked long and hard to learn how well a line fits data.
  (Lines are relatively simple, and you can even bring that along to more
  complicated models.)

- But when you start talking about something like a neural net with 16 hidden
  layers, there's no statistician in the world that can write out the analytic
  statistics of how that model fits the data. (In other words, in Machine
  Learning we're working with models where you can't really do the analytic
  statistical distribution of the results - it's not like fitting a line to data
  where you can write down the sampling distribution; if you're doing something
  like a random forest or a neural net, it's not something that you can compute
  analytically very easily.)

Notes:
- CV is the go-to method for model evaluation in Machine Learning, because
  statistics of the models are often not known in the classical sense.

- Again: caveats about selection bias and independence in data.
"""