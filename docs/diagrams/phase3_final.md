# Faz 3 — Strategy + Observer + CI (Final Mimari)

Runtime'da algoritma değişimi Strategy ile, olay bildirimi Observer ile sağlandı.

```mermaid
classDiagram
    class EncryptionStrategy {
        -_algorithm: EncryptionAlgorithm
        +set_algorithm(algorithm)
        +encrypt(text) str
        +decrypt(text) str
    }

    class EncryptionEventManager {
        -_listeners: dict
        +subscribe(event, listener)
        +unsubscribe(event, listener)
        +notify(event, data)
    }

    class EventListener {
        <<interface>>
        +update(event, data)
    }

    class ConsoleLogger {
        +update(event, data)
    }

    class StatisticsCollector {
        -stats: dict
        +update(event, data)
        +get_stats() dict
    }

    class Encryptor {
        -strategy: EncryptionStrategy
        -factory: AlgorithmFactory
        -event_manager: EncryptionEventManager
        +encrypt(text) str
        +decrypt(text) str
        +set_algorithm(name)
    }

    class AlgorithmFactory {
        -_algorithms: dict
        +register(name, cls)
        +create(name) EncryptionAlgorithm
    }

    Encryptor --> EncryptionStrategy : delegates
    Encryptor --> AlgorithmFactory : creates via
    Encryptor --> EncryptionEventManager : notifies
    EncryptionStrategy --> EncryptionAlgorithm : uses
    EventListener <|.. ConsoleLogger
    EventListener <|.. StatisticsCollector
    EncryptionEventManager --> EventListener : notifies
