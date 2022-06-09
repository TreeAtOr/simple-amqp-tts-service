# TTS microservice container

[SileroAI TTS model](https://github.com/snakers4/silero-models) for pytorch wrapped in python microservice comunicates via AMQP protocol. 

Service stores TTS file in container filesystem as some kind of cache and can be accesed via HTTP or FTP protocols.

## Messages
### Consuming
#### To order new TTS task
```json
{
    "type": "tts",
    "id": "your request id",
    "content": "SSML content"
}
```

#### To free cached result
```json
{
    "type": "free",
    "id": "you request id"
}
```

### Produsing
#### When TTS file ready
```json
{
    "type": "ready",
    "id": "you request id"
}
```

#### When an error in TTS request
```json
{
    "type": "tts",
    "id": "your request id",
    "content": "error details"
}
```

