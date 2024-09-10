# ai-chatbot-be

# Follow clean archietecture:

* Layered archietecture

* Isolate the business rules: (presentation(application(domain))infrastructure) 

* Infrastructures such as: frameworks, technologies, database, UI,.. located in outer layer (Can be changed and extended)

* outer layers depend on inner layers

* Components'change does not affect the core

/domain
Domain Layer (Entities): Chứa các đối tượng cốt lõi và logic nghiệp vụ cơ bản của hệ thống. Đây là tầng độc lập và có thể dùng lại trong nhiều bối cảnh.

/application
Application Layer (Use Cases): Xử lý các quy tắc nghiệp vụ cụ thể. Đây là nơi các luồng nghiệp vụ xảy ra, và tương tác với các repository interface để lấy dữ liệu.

/presentation
Presentation Layer (UI): Giao diện người dùng, bao gồm controller, các API hoặc web UI để nhận yêu cầu và trả về kết quả.

/infrastructure
Infrastructure Layer: Chứa các thành phần kỹ thuật như kết nối cơ sở dữ liệu, API bên ngoài, và các cài đặt chi tiết về repository.
