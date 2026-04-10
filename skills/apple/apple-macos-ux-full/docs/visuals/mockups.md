# Visual Examples / Mockups

```
+--------------------------------------------------------------+
|  ●  ●  ●        Project — Unified Toolbar                    |
|  [New]                 [Search field..................]      |
+----------------------+---------------------------------------+
| ▸ Sidebar             |  Detail                              |
|   • Inbox             |  Title                               |
|   • Today             |  Content area                         |
|   • Starred           |                                       |
+----------------------+---------------------------------------+
```

```mermaid
flowchart LR
  Sidebar -->|selection| Detail
  Toolbar -->|actions| FirstResponder
  MenuBar -->|nil target| FirstResponder
  FirstResponder --> Controller
  Controller --> Model
```
