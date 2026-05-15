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
```

## Tüm Fazların Özeti

| Faz | Pattern | Çözülen Sorun |
|-----|---------|---------------|
| 0 | — | Sorun tespiti (PROBLEMS.md) |
| 1 | Factory Method | Nesne yaratma, if-else zincirleri |
| 2 | Adapter + Decorator | Harici entegrasyon, ek davranışlar |
| 3 | Strategy + Observer | Runtime değişimi, olay bildirimi |

## CI Pipeline

GitHub Actions ile her push'ta otomatik test çalıştırılıyor (`pytest`).
