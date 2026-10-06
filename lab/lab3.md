## Question 1

In the MLflow UI (Model training → Model registry), my registered model `food11` shows **Latest version: Version 1** with the alias `@champion → Version 1`. So my model was given version `1`.

A run's logged model artifact belongs to one specific MLflow training run. It is stored as part of that run's outputs ➕(the model files such as the `MLmodel` metadata, the pickled PyTorch model and its requirements), and it is identified only by the run ID (`runs:/<run-id>/model`). Every training run I did in Lab 2 logged its own model artifact, whether it was good or bad.

A registered model is a separate entry in the MLflow Model Registry with its own name and version number, such as `food11` version `1`. ➕It points back to the run artifact it came from, but it adds model-management information: an automatic version history (1, 2, 3, …), aliases (like `champion`), tags and a description. Only the models I choose to promote (my best run by `val_accuracy`) become registered versions.

This makes it easier to manage and promote models independently from the training run that originally produced them ➕, and to load them by name (`models:/food11@champion`) instead of by a run ID.


## Question 2

MLflow now uses aliases instead of the old built-in stages such as `Staging` and `Production` ➕(the old stages were a fixed list: None, Staging, Production, Archived). Aliases are custom names like `champion` or `challenger`, and MLflow also supports free-form tags for any other information.

In my project, I assigned the alias `champion` to version 1 of the `food11` model.

A model is versioned separately from the training run so different model versions can be managed under one registered model name. ➕A run is a record of one experiment (parameters, metrics, artifacts), and most runs are never deployed. Versioning the model separately keeps a clean history of only the models worth serving. It also lets the serving code refer to a stable name (`food11`) instead of a random run ID, and makes it easy to go back to an older version if a new one performs badly.

An alias is flexible because it can be moved to another model version later without changing the application code that loads `models:/food11@champion`. ➕Unlike fixed stages, I can choose any alias names and use several at once (for example `champion` for the production model and `challenger` for a candidate being tested). Each alias points to exactly one version at a time. Promoting a new model, or rolling back to the old one, just means moving the alias. The version numbers themselves never change.
