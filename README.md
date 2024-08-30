# ai-chatbot-be

# Follow clean archietecture:

* Layered archietecture

* Isolate the business rules: (adapters(application(domain))) 

* Infrastructures such as: frameworks, technologies, database, UI,.. located in outer layer (Can be changed and extended)

* outer layers depend on inner layers

* Components'change does not affect the core

/domain
This layer represents the core business logic and rules of the application, and it is independent of any frameworks or external services.

/application
This layer contains the application-specific business logic, focusing on orchestrating the domain logic according to the application's use cases.

/adapters
This layer handles the conversion of data and requests from the outside world into a form that the application can process, and vice versa.

/infrastructure
This layer contains the concrete implementations of the interfaces defined in the domain layer and manages interaction with external services and databases.
