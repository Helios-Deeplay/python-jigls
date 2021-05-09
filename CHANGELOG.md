# Changelog

## [0.5.1] - 2021-05-09

### Added

- check duplicate edges
- deleting items from scene
- editting edges, reconnecting
- implement serialization
- implement deserialization
- mutli sockets diffrent shape

### Changed

- rework socket manager class
- rework node
- rework edge class
- refactor all classes to properly use properties

### Fixed

- dragging edge different style
- double check newly added edges if the sockets are updated properly

## [0.4.2] - 2021-05-02

### Added

- Scene manager
- Socket manager
- Dragging and creating edges
- Movables graphicitems
- Simple node content template

### Fixed

- edges added to non multiconnection socket. socket list was not being updated
## [0.3.0] - 2021-03-27

### Added

- basic graphic item implementation for node editor
- new logic simulation using computational graph

### Changed

- computational graph implementaion
### Fixed

- Fixed item

### Removed

- [logic simulation implementation](https://openbookproject.net/courses/python4fun/logic.html)