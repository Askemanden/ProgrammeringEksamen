# Board.py Flowcharts

## `Board.__init__`

```mermaid
flowchart TD

    A(["Start 'Board.__init__'"])

    A2[/"Arguments:
    settings: GameSettings
    premade_board_pos: Optional[List[List[BoardSpace]]] = None"
    /]

    B["Set self.settings = settings"]

    C["Initialize board_tiles, previous_board_state, captures"]

    D{"premade_board_pos == None?"}

    E["premade_board_pos = []"]

    F{"len(premade_board_pos) != board_size?"}

    G["board_tiles = __populate_board_tiles()"]

    H["Print 'standardbræt oprettet'"]

    I["success = True"]

    J["For each row in premade_board_pos:"]

    K{"len(row) != board_size?"}

    L["success = False"]

    M["Break"]

    N["End for"]

    O{"success?"}

    P["board_tiles = deepcopy(premade_board_pos)"]

    Q["Print 'Specielt bræt oprettet'"]

    R["board_tiles = __populate_board_tiles()"]

    S["Print 'Bræt givet af forkert størrelse | Standardbræt oprettet'"]

    T["previous_board_state = deepcopy(board_tiles)"]

    U(["End"])

    A --> A2
    A2 --> B
    B --> C
    C --> D

    D -->|Yes| E
    D -->|No| F

    E --> F
    F -->|Yes| G
    F -->|No| I

    G --> H
    H --> T

    I --> J
    J --> K

    K -->|Yes| L
    K -->|No| N

    L --> M
    M --> N

    N --> O
    O -->|Yes| P
    O -->|No| R

    P --> Q
    Q --> T

    R --> S
    S --> T

    T --> U
```

## `__populate_board_tiles`

```mermaid
flowchart TD

    A(["Start '__populate_board_tiles'"])

    B["columns = []"]

    C["For _ in 0..board_size-1:"]

    D["row = []"]

    E["For _ in 0..board_size-1:"]

    F["row.append(EMPTY)"]

    G["End for"]

    H["columns.append(row)"]

    I["End for"]

    J["Return columns"]

    K(["End"])

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
```

## `__out_of_bounds`

```mermaid
flowchart TD

    A(["Start '__out_of_bounds'"])

    A2[/"Arguments:
    x: int
    y: int"
    /]

    B{"x < 0 or x >= board_size?"}

    C["Return True"]

    D{"y < 0 or y >= board_size?"}

    E["Return True"]

    F["Return False"]

    G(["End"])

    A --> A2
    A2 --> B

    B -->|Yes| C
    B -->|No| D

    D -->|Yes| E
    D -->|No| F

    C --> G
    E --> G
    F --> G
```

## `__get_adjacent_positions`

```mermaid
flowchart TD

    A(["Start '__get_adjacent_positions'"])

    A2[/"Arguments:
    x: int
    y: int"
    /]

    B["positions = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]"]

    C["valid_positions = []"]

    D["For px, py in positions:"]

    E{"not __out_of_bounds(px, py)?"}

    F["valid_positions.append((px, py))"]

    G["End for"]

    H["Return valid_positions"]

    I(["End"])

    A --> A2
    A2 --> B
    B --> C
    C --> D
    D --> E

    E -->|Yes| F
    E -->|No| G

    F --> G
    G --> H
    H --> I
```

## `__get_group`

```mermaid
flowchart TD

    A(["Start '__get_group'"])

    A2[/"Arguments:
    x: int
    y: int"
    /]

    B["colour = board_tiles[x][y]"]

    C["visited = set()"]

    D["stack = [(x, y)]"]

    E["While stack:"]

    F["cx, cy = stack.pop()"]

    G{"(cx, cy) in visited?"}

    H["Continue"]

    I["visited.add((cx, cy))"]

    J["neighbours = __get_adjacent_positions(cx, cy)"]

    K["For nx, ny in neighbours:"]

    L{"board_tiles[nx][ny] == colour?"}

    M["stack.append((nx, ny))"]

    N["End for"]

    O["End while"]

    P["Return Group(colour, list(visited))"]

    Q(["End"])

    A --> A2
    A2 --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G

    G -->|Yes| H
    G -->|No| I
    I --> J
    J --> K
    K --> L

    L -->|Yes| M
    L -->|No| N

    M --> N
    N --> O
    O --> P
    P --> Q

    H --> E
```

## `__group_has_liberties`

```mermaid
flowchart TD

    A(["Start '__group_has_liberties'"])

    A2[/"Arguments:
    group: Group"
    /]

    B["For x, y in group.members:"]

    C["neighbours = __get_adjacent_positions(x, y)"]

    D["For nx, ny in neighbours:"]

    E{"board_tiles[nx][ny] == EMPTY?"}

    F["Return True"]

    G["End for inner"]

    H["End for outer"]

    I["Return False"]

    J(["End"])

    A --> A2
    A2 --> B
    B --> C
    C --> D
    D --> E

    E -->|Yes| F
    E -->|No| G

    G --> H
    H --> I
    I --> J

    F --> J
```

## `__remove_group`

```mermaid
flowchart TD

    A(["Start '__remove_group'"])

    A2[/"Arguments:
    group: Group"
    /]

    B{"group.colour == WHITE?"}

    C["black_captures += len(group.members)"]

    D["white_captures += len(group.members)"]

    E["For x, y in group.members:"]

    F["board_tiles[x][y] = EMPTY"]

    G["End for"]

    H(["End"])

    A --> A2
    A2 --> B

    B -->|Yes| C
    B -->|No| D

    C --> E
    D --> E
    E --> F
    F --> G
    G --> H
```

## `__board_equals`

```mermaid
flowchart TD

    A(["Start '__board_equals'"])

    A2[/"Arguments:
    board_a: List[List[BoardSpace]]
    board_b: List[List[BoardSpace]]"
    /]

    B["For x in 0..board_size-1:"]

    C["For y in 0..board_size-1:"]

    D{"board_a[x][y] != board_b[x][y]?"}

    E["Return False"]

    F["End for y"]

    G["End for x"]

    H["Return True"]

    I(["End"])

    A --> A2
    A2 --> B
    B --> C
    C --> D

    D -->|Yes| E
    D -->|No| F

    F --> G
    G --> H
    H --> I

    E --> I
```

## `__get_opposite_colour`

```mermaid
flowchart TD

    A(["Start '__get_opposite_colour'"])

    A2[/"Arguments:
    stone: BoardSpace"
    /]

    B{"stone == BLACK?"}

    C["Return WHITE"]

    D{"stone == WHITE?"}

    E["Return BLACK"]

    F["Return EMPTY"]

    G(["End"])

    A --> A2
    A2 --> B

    B -->|Yes| C
    B -->|No| D

    D -->|Yes| E
    D -->|No| F

    C --> G
    E --> G
    F --> G
```

## `place_stone`

```mermaid
flowchart TD

    A(["Start 'place_stone'"])

    A2[/"Arguments:
    x: int
    y: int
    stone: BoardSpace"
    /]

    B{"__out_of_bounds(x, y)?"}

    C["Return False"]

    D{"board_tiles[x][y] != EMPTY?"}

    E["Return False"]

    F["old_board = deepcopy(board_tiles)"]

    G["board_tiles[x][y] = stone"]

    H["opponent_colour = __get_opposite_colour(stone)"]

    I["checked_positions = set()"]

    J["neighbours = __get_adjacent_positions(x, y)"]

    K["For nx, ny in neighbours:"]

    L{"board_tiles[nx][ny] != opponent_colour?"}

    M["Continue"]

    N{"(nx, ny) in checked_positions?"}

    O["Continue"]

    P["enemy_group = __get_group(nx, ny)"]

    Q["For member in enemy_group.members:"]

    R["checked_positions.add(member)"]

    S["End for"]

    T{"not __group_has_liberties(enemy_group)?"}

    U["__remove_group(enemy_group)"]

    V["End for"]

    W["own_group = __get_group(x, y)"]

    X{"not __group_has_liberties(own_group)?"}

    Y["board_tiles = old_board"]

    Z["Return False"]

    AA["If __board_equals(board_tiles, previous_board_state):"]

    BB["board_tiles = old_board"]

    CC["Return False"]

    DD["previous_board_state = old_board"]

    EE["Return True"]

    FF(["End"])

    A --> A2
    A2 --> B

    B -->|Yes| C
    B -->|No| D

    D -->|Yes| E
    D -->|No| F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L

    L -->|Yes| M
    L -->|No| N

    M --> V
    N -->|Yes| O
    N -->|No| P
    P --> Q
    Q --> R
    R --> S
    S --> T

    T -->|Yes| U
    T -->|No| V

    U --> V
    V --> W
    W --> X

    X -->|Yes| Y
    X -->|No| AA

    Y --> Z
    Z --> FF

    AA --> BB
    BB --> CC
    CC --> FF

    AA --> DD
    DD --> EE
    EE --> FF

    C --> FF
    E --> FF
```

## `remove_stone`

```mermaid
flowchart TD

    A(["Start 'remove_stone'"])

    A2[/"Arguments:
    x: int
    y: int"
    /]

    B{"__out_of_bounds(x, y)?"}

    C["Return False"]

    D["board_tiles[x][y] = EMPTY"]

    E["Return True"]

    F(["End"])

    A --> A2
    A2 --> B

    B -->|Yes| C
    B -->|No| D
    D --> E
    E --> F

    C --> F
```

## `print_board`

```mermaid
flowchart TD

    A(["Start 'print_board'"])

    B["symbols = {BLACK: 'B', WHITE: 'W', EMPTY: '.'}"]

    C["For y in 0..board_size-1:"]

    D["row = ''"]

    E["For x in 0..board_size-1:"]

    F["row += symbols[board_tiles[x][y]] + ' '"]

    G["End for x"]

    H["Print row"]

    I["End for y"]

    J["Print ''"]

    K(["End"])

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
```

## `calculate_score`

```mermaid
flowchart TD

    A(["Start 'calculate_score'"])

    A2[/"Arguments:
    original_board: Board
    territory_board: Board"
    /]

    B["black_score = 0, white_score = 0"]

    C["For x in 0..original_board.board_size-1:"]

    D["For y in 0..original_board.board_size-1:"]

    E["original_space = original_board.board_tiles[x][y]"]

    F["territory_space = territory_board.board_tiles[x][y]"]

    G{"original_space != EMPTY?"}

    H["Continue"]

    I{"territory_space == BLACK?"}

    J["black_score += 1"]

    K{"territory_space == WHITE?"}

    L["white_score += 1"]

    M["End for y"]

    N["End for x"]

    O["white_score += original_board.white_captures"]

    P["black_score += original_board.black_captures"]

    Q["Return (black_score, white_score)"]

    R(["End"])

    A --> A2
    A2 --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G

    G -->|Yes| H
    G -->|No| I

    H --> M
    I -->|Yes| J
    I -->|No| K

    K -->|Yes| L
    K -->|No| M

    J --> M
    L --> M
    M --> N
    N --> O
    O --> P
    P --> Q
    Q --> R
```
