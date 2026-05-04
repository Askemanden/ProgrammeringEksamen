## `evaluate_values`

```mermaid
flowchart TD

    A(["Start 'evaluate_values'"])

    A2[/"Arguments:
    board: Board
    dilations: int = 5
    erosions: Optional[int] = None"
    /]

    B{"'erosions' is None?"}

    C["Set default erosion count"]

    D["Initialize Bouzy values"]

    E{"More dilation iterations?"}
    F["Apply '__dilate_z'"]

    G{"More erosion iterations?"}
    H["Apply '__erase_z'"]

    I["Return values"]

    J(["End"])

    A --> A2
    A2 --> B

    B -->|Yes| C
    B -->|No| D

    C --> D

    D --> E

    E -->|Yes| F
    F --> E

    E -->|No| G

    G -->|Yes| H
    H --> G

    G -->|No| I

    I --> J
```

---

## `evaluate_territory_board`

```mermaid
flowchart TD

    A(["Start 'evaluate_territory_board'"])

    A2[/"Arguments:
    board: Board
    dilations: int = 5
    erosions: Optional[int] = None"
    /]

    B["Evaluate Bouzy values"]

    C["Deep copy board"]

    D{"More board positions?"}

    E{"Tile is EMPTY?"}

    F["Skip tile"]

    G["Read evaluated value"]

    H{"Value > 0?"}
    I["Set BLACK territory"]

    J{"Value < 0?"}
    K["Set WHITE territory"]

    L["Set EMPTY territory"]

    M["Return territory board"]

    N(["End"])

    A --> A2
    A2 --> B

    B --> C

    C --> D

    D -->|Yes| E

    E -->|No| F
    F --> D

    E -->|Yes| G

    G --> H

    H -->|Yes| I
    I --> D

    H -->|No| J

    J -->|Yes| K
    K --> D

    J -->|No| L
    L --> D

    D -->|No| M

    M --> N
```

---

## `print_values`

```mermaid
flowchart TD

    A(["Start 'print_values'"])

    A2[/"Arguments:
    values: List[List[int]]"
    /]

    B["Get board size"]

    C{"More rows?"}

    D["Create row buffer"]

    E{"More columns?"}

    F["Read current value"]

    G{"Value >= 0?"}

    H["Append formatted positive value"]

    I["Append formatted negative value"]

    J["Print row"]

    K(["End"])

    A --> A2
    A2 --> B

    B --> C

    C -->|Yes| D
    D --> E

    E -->|Yes| F
    F --> G

    G -->|Yes| H
    H --> E

    G -->|No| I
    I --> E

    E -->|No| J
    J --> C

    C -->|No| K
```

---

## `__initialize_values`

```mermaid
flowchart TD

    A(["Start '__initialize_values'"])

    A2[/"Arguments:
    board: Board"
    /]

    B["Get board size"]

    C["Create empty values list"]

    D{"More columns?"}

    E["Create empty column"]

    F{"More rows?"}

    G["Read board tile"]

    H{"Tile is BLACK?"}

    I["Append BLACK_VALUE"]

    J{"Tile is WHITE?"}

    K["Append WHITE_VALUE"]

    L["Append 0"]

    M["Append column to values"]

    N["Return values"]

    O(["End"])

    A --> A2
    A2 --> B

    B --> C

    C --> D

    D -->|Yes| E
    E --> F

    F -->|Yes| G
    G --> H

    H -->|Yes| I
    I --> F

    H -->|No| J

    J -->|Yes| K
    K --> F

    J -->|No| L
    L --> F

    F -->|No| M
    M --> D

    D -->|No| N

    N --> O
```

---

## `__dilate_z` — Part 1

```mermaid
flowchart TD

    A(["Start '__dilate_z'"])

    A2[/"Arguments:
    values: List[List[int]]"
    /]

    B["Copy values into result"]

    C{"More board positions?"}

    D["Read current value"]

    E["Get neighbour values"]

    F["Determine neighbour signs"]

    G{"Mixed or no neighbour signs?"}

    H["Skip position"]

    I["Determine dominant sign"]

    J{"Current conflicts with sign?"}

    K["Count supporting neighbours"]

    L{"Current == 0?"}

    M["Create new value from support"]

    N{{"Continue Value Update"}}

    O(["End"])

    A --> A2
    A2 --> B

    B --> C

    C -->|Yes| D

    D --> E
    E --> F

    F --> G

    G -->|Yes| H
    H --> C

    G -->|No| I

    I --> J

    J -->|Yes| H

    J -->|No| K

    K --> L

    L -->|Yes| M
    M --> N

    L -->|No| N

    C -->|No| O
```

---

## `__dilate_z` — Part 2

```mermaid
flowchart TD

    A{{"Continue Value Update"}}

    B{"Current == 0?"}

    C["Clamp and store support value"]

    D["Increase magnitude"]

    E["Clamp and store updated value"]

    F["Return to main iteration"]

    G(["End"])

    A --> B

    B -->|Yes| C
    C --> F

    B -->|No| D

    D --> E
    E --> F

    F --> G
```

---

## `__erase_z` — Part 1

```mermaid
flowchart TD

    A(["Start '__erase_z'"])

    A2[/"Arguments:
    values: List[List[int]]"
    /]

    B["Copy values into result"]

    C{"More board positions?"}

    D["Read current value"]

    E{"Current == 0?"}

    F["Skip position"]

    G["Determine sign and magnitude"]

    H["Get neighbour values"]

    I["Calculate erosion amount"]

    J["Reduce magnitude"]

    K{"Magnitude <= 0?"}

    L{{"Finalize Eroded Value"}}

    M(["End"])

    A --> A2
    A2 --> B

    B --> C

    C -->|Yes| D

    D --> E

    E -->|Yes| F
    F --> C

    E -->|No| G

    G --> H
    H --> I
    I --> J

    J --> K

    K -->|Yes| L
    K -->|No| L

    C -->|No| M
```

---

## `__erase_z` — Part 2

```mermaid
flowchart TD

    A{{"Finalize Eroded Value"}}

    B{"Magnitude <= 0?"}

    C["Set value to 0"]

    D["Clamp and store updated value"]

    E["Return to main iteration"]

    F(["End"])

    A --> B

    B -->|Yes| C
    C --> E

    B -->|No| D
    D --> E

    E --> F
```

## `__get_neighbour_values`

```mermaid
flowchart TD

    A(["Start '__get_neighbour_values'"])

    A2[/"Arguments:
    values: List[List[int]]
    x: int
    y: int"
    /]

    B["Create empty neighbours list"]

    C["Create orthogonal directions"]

    D{"More directions?"}

    E["Calculate neighbour coordinates"]

    F{"Coordinates inside bounds?"}

    G["Append neighbour value"]

    H["Return neighbours"]

    I(["End"])

    A --> A2
    A2 --> B

    B --> C

    C --> D

    D -->|Yes| E

    E --> F

    F -->|Yes| G
    G --> D

    F -->|No| D

    D -->|No| H

    H --> I
```

---

## `__clamp`

```mermaid
flowchart TD

    A(["Start '__clamp'"])

    A2[/"Arguments:
    value: int"
    /]

    B{"Value > 64?"}

    C["Return 64"]

    D{"Value < -64?"}

    E["Return -64"]

    F["Return original value"]

    G(["End"])

    A --> A2
    A2 --> B

    B -->|Yes| C
    C --> G

    B -->|No| D

    D -->|Yes| E
    E --> G

    D -->|No| F
    F --> G
```