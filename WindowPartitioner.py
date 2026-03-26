import pygame
import json

# INFO-Klasser

class UI_info():                                                        # Basisklasse for alle info og udvidelsesklasser til et komponent.
    def __init__ (self):
        pass
    def update(self):
        pass
    def event_handling(self, event):
        pass
    def draw(self, screen):
        pass

class UI_component_placement_info(UI_info):
    def __init__(self, x, y, width, height, anchor_x = "left", anchor_y = "top"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

class UI_component_color_info(UI_info):
    def __init__(self, primary_color = (100, 149, 237), secondary_color = (0, 70, 148), accent_color = (227, 209, 120)):
        self.primary_color = (abs(primary_color[0] % 255), abs(primary_color[1] % 255), abs(primary_color[2] % 255))
        self.secondary_color = (abs(secondary_color[0] % 255), abs(secondary_color[1] % 255), abs(secondary_color[2] % 255))
        self.accent_color = (abs(accent_color[0] % 255), abs(accent_color[1] % 255), abs(accent_color[2] % 255))
        self.primary_complementary_color = (255 - primary_color[0], 255 - primary_color[1], 255 - primary_color[2])
        self.secondary_complementary_color = (255 - secondary_color[0], 255 - secondary_color[1], 255 - secondary_color[2])

# UDVIDELSES-Klasser

class UI_component_text(UI_info):
    def __init__(self, component, text = "Hej verden", size = 20):
        self.component = component
        self.text = text
        if size != None:
            self.size = size
        else:
            self.size = 20
        self.font = pygame.font.SysFont('yu_gothic', self.size)
        self.bold_font = pygame.font.SysFont('yu_gothic', self.size, bold=True)
        self.bold = False

    def get_text_color(self):
        r = 0; b = 0; g = 0
        if self.component.color_info != None and self.component.visible:
            r = self.component.color_info.primary_color[0]
            g = self.component.color_info.primary_color[1]
            b = self.component.color_info.primary_color[2]
        elif self.component.visible:
            r = self.component.parent_box.color_info.secondary_color[0]
            g = self.component.parent_box.color_info.secondary_color[1]
            b = self.component.parent_box.color_info.secondary_color[2]
        else:
            r = self.component.parent_box.color_info.primary_color[0]
            g = self.component.parent_box.color_info.primary_color[1]
            b = self.component.parent_box.color_info.primary_color[2]
        
        luminans = 0.2126 * r + 0.7152 * g + 0.0722 * b

        # Hvis baggrunden er lys → brug mørkegrå
        if luminans > 130:
            return (20, 20, 20)  # mørkegrå

        # Hvis baggrunden er mørk → brug hvid
        return (230, 230, 230)  # hvid

    def update(self):
        if self.component.hovered:
            self.bold = True
        else:
            self.bold = False

    def draw(self, screen):
        image = self.font.render(self.text, True, self.get_text_color())
        self.text_rect = image.get_rect()
 
        if self.bold:
            text_surface = self.bold_font.render(self.text, True, self.get_text_color(), None)
        else:
            text_surface = self.font.render(self.text, True, self.get_text_color(), None)
        screen.blit(text_surface, (self.component.rect.x  + (0.5 * (self.component.rect.width - self.text_rect.width)), self.component.rect.y + self.component.rect.height * 0.2))

class UI_button_extension(UI_info):
    def __init__(self, component, function_id : str = "intet", function_map : dict = {}):
        self.function_id = function_id
        self.component = component
        self.function_map = function_map

    def event_handling(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.component.rect.collidepoint(event.pos):
                fcunt = self.function_map.get(self.function_id, intet)
                fcunt()

    def update(self):
        if self.component.rect.collidepoint(pygame.mouse.get_pos()):   
            self.component.hovered = True
        else:
            self.component.hovered = False

# UI-Komponenter

class UI_component:                                         # Basisklasse for alle UI komponenter til et UI_element.
    def __init__(self, placement_info: UI_component_placement_info, color_info: UI_component_color_info, parent_box : "screen_box", visible = True):
        self.color_info = color_info
        self.hovered = False
        self.placement_info = placement_info
        self.text = UI_info()
        self.button = UI_info()
        self.parent_box = parent_box
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.visible = visible
        if visible:
            self.drawing_method = self.drawing_helper_visible
        else:
            self.drawing_method = self.drawing_helper_invisible

    def update_color(self):
        if self.color_info == None :
            self.color_info = self.parent_box.color_info

    def update(self):
        #self.color_info.update()
        #self.placement_info.update()
        self.text.update()
        if self.button != None:
            self.button.update()

    def event_handling(self, event):
        self.button.event_handling(event)

    def draw_visible(self, screen : pygame.Surface):
        color_source = self.color_info.primary_color
        accent_color = self.color_info.accent_color
        
        #pygame.draw.rect(screen, (100, 100, 100), self.rect)
        if self.hovered:
            #brighter_color = (min(color_source.secondary_color[0] + 40, 255), min(color_source.secondary_color[1] + 40, 255), min(color_source.secondary_color[2] + 40, 255))
            brighter_color = accent_color
            pygame.draw.rect(screen, brighter_color, self.rect)
        else:
            pygame.draw.rect(screen, color_source, self.rect)
        self.text.draw(screen)

    def draw_invisible(self, screen : pygame.Surface):
        self.text.draw(screen)

    def drawing_helper_invisible(self):
        self.draw_invisible(self.screen)

    def drawing_helper_visible(self):
        self.draw_visible(self.screen)

    def draw(self, screen : pygame.Surface):
       self.screen = screen
       self.drawing_method()

# UI-Element

class UI_element:                                                       # Basisklasse for alle UI elementer.
    def __init__(self, placement : UI_component_placement_info):
        self.screen_position_x = placement.x - placement.width * 0.5
        self.screen_position_y = placement.y - placement.height * 0.5
        self.rect = pygame.Rect(self.screen_position_x, self.screen_position_y, placement.width, placement.height)                           # Basisklasse har en rektangel.
        self.color_info = UI_info()

    def update(self):
        pass

    def move(self, x : int, y : int):
        pass

    def draw(self, screen : pygame.Surface):
        pass

class screen_box (UI_element):                                       # En boks på skærmen der kan indeholde knapper og items.
    def __init__(self, placement : UI_component_placement_info, color : UI_component_color_info, border_width = 8):
        super().__init__(placement)
        #self.screen_position_x = placement.x - placement.width * 0.5
        #self.screen_position_y = placement.y - placement.height * 0.5
        #self.rect = pygame.Rect(self.screen_position_x, self.screen_position_y, placement.width, placement.height)

        self.border_width = border_width
        
        self.color_info = color
        self.fill_color = self.color_info.primary_color
        self.border_color = color.accent_color
       
        self.components = []
        self.number_of_buttons = 0                                      # Antallet af automatisk placerede knapper i listen af containere. Bruges til at arrangere knapperne jævnt.

    def create_UIcomponent(self, color : UI_component_color_info, placement_info : UI_component_placement_info, text = "", text_size = 20, function = None, visible : bool = True, function_map : dict = {}):
        if color == None:
            color = UI_component_color_info(self.color_info.secondary_color, self.color_info.primary_color, self.color_info.accent_color)
        component = UI_component(placement_info, color, self, visible)
        text_object = UI_component_text(component, text, text_size)
        component.text = text_object
        if function != None:
            button_object = UI_button_extension(component, function, function_map)
            component.button = button_object

        self.components.append(component)
        self.place_all_components()
    
    def count_buttons(self):                                            # Tæller antallet af automatisk placerede knapper i listen af containere.
        count = 0
        for container in self.components:
            if not isinstance(container.placement_info, UI_component_placement_info) and isinstance(container.button, UI_button_extension):
                count += 1
        self.number_of_buttons = count

    def remove_container(self, container):                              # Fjerner en container fra listen af containere.
        pass # TODO

    def update(self):                                                   # Opdaterer tilstanden af screen_boxen og dens containere.
                                                                        # update kalder ikke den matematiktunge place_all_buttons, da den kun behøver at blive kaldt når en container tilføjes eller fjernes, eller kassen flyttes.
        for container in self.components:
           container.update()
        #for event in pygame.event.get():
        #    for component in self.components:
        #        component.event_handling(event)

    def place_component(self, component, automatic_button_index):       # sætter x og y positionen for en knap baseret på dens placering KUN i forhold til andre af dens type.
                                                                        # Bredden og højden beregnes af screen_boxen, da dette er lettere.
        if component.placement_info != None:   # Component er en knap med manuel layout info.

            if component.placement_info.anchor_x == "center":
                component.rect.x = self.rect.x + (self.rect.width - component.placement_info.width) * 0.5 + component.placement_info.x
            else:
                component.rect.x = self.rect.x + component.placement_info.x

            if component.placement_info.anchor_y == "center":
                component.rect.y = self.rect.y + (self.rect.height - component.placement_info.height) * 0.5 + component.placement_info.y
            else:
                component.rect.y = self.rect.y + component.placement_info.y

        else:
            if component.button != None:
                button_height = component.rect.height
                button_width = component.rect.width
                component.rect.x = self.rect.x + self.border_width + automatic_button_index * (button_width + self.border_width)
                component.rect.y = self.rect.y + self.rect.height - self.border_width - button_height

            #elif isinstance(component, label):
            #    component.rect.x = self.rect.x + self.border_width
            #    component.rect.y = self.rect.y + self.border_width
            #    component.rect.width = self.rect.width - self.border_width * 2
            #    component.rect.height = self.rect.height - (self.border_width * 2 + 40 * 1.2) # 40 er standarden for knaphøjde. TODO: Gør dette dynamisk baseret på screen_boxens højde.
    
    def place_all_components(self):
        self.count_buttons()
        automatic_button_index = 0

        for container in self.components:

            if container.placement_info == None:
                if container.button != None:    # Automatisk placeret knap.
                    container.rect.width = (self.rect.width - self.border_width * (self.number_of_buttons + 1)) / self.number_of_buttons
                    container.rect.height = 40 # Standard højde for knapper. TODO: Gør dette dynamisk baseret på screen_boxens højde.
                    automatic_button_index += 1
                else:
                    pass
                    # Det er ikke en automatisk placeret knap.
                    #TODO implementer håndtering af komponenter uden placement_info der ikke er en knap
            else:
                container.rect.width = container.placement_info.width
                container.rect.height = container.placement_info.height

            self.place_component(container, automatic_button_index - 1)  # -1 fordi indexet er blevet forøget efter placeringen af knappen.
                
    def move(self, x, y):
        self.screen_position_x = int(x - self.rect.width * 0.5)
        self.screen_position_y = int(y - self.rect.height * 0.5)
        self.rect.topleft = (self.screen_position_x, self.screen_position_y)
        self.place_all_components()

    def event_handler(self, event):
        for component in self.components:
            component.event_handling(event)

    def draw(self, screen):
        # Tegner en boks med en kant. Kanten er border_width pixels bred.
        border_rect = pygame.Rect(self.rect.left - self.border_width, self.rect.top - self.border_width, self.rect.width + self.border_width * 2, self.rect.height + self.border_width * 2)
        pygame.draw.rect(screen, self.border_color, border_rect)
        pygame.draw.rect(screen, self.fill_color, self.rect)

        # Tegner alle UI-komponenter i boksen.
        # For nu arrangeres alle knapper, vandret i bunden af boksen. Lidt ligesom Windows pop-up menuer.
        # Alle andre UI-komponenter arrangeres lodret i toppen af boksen, og der kan scrolles gennem dem.
        for container in self.components:
            container.draw(screen)

class dropdown(screen_box):
    def __init__(self, placement : UI_component_placement_info, color : UI_component_color_info):
        super().__init__(placement, color)
        self.placement_info = placement
        self.color_info = color

# Return of the king...
def intet():
    pass

class Game():
    def __init__(self, function_map : dict = {}):
        self.running = True
        self.esc_menu = False

        self.active_menu = 0
        self.active_esc_menu = 0

        self.menus = []
        self.HUD_elements = []
        self.esc_menu_elements = []

        self.function_map = function_map

    def toggle_menu(self):
        self.active_menu = self.active_menu + 1
        if self.active_menu > len(self.menus) - 1:
            self.active_menu = 0

    def switch_menu(self, menu_index : int):
        
        if not menu_index > len(self.menus) - 1 and menu_index > -1:
            self.active_menu = menu_index
    
    def switch_esc_menu(self, esc_menu_index : int):
        if not esc_menu_index > len(self.esc_menu_elements) - 1 and esc_menu_index > -1:
            self.active_esc_menu = esc_menu_index

    def save_menu_layout(self, output : str = "saved_menu.json"):
        temp_menu_dict = {}
        
        screen_box_list = []
        for i in range (len(self.menus)):
            screen_box_list.append(create_json_from_menu(self.menus[i]))
        
        temp_menu_dict[f"screen_boxes"] = screen_box_list

        esc_menu_list = []
        for j in range (len(self.esc_menu_elements)):
          esc_menu_list.append(create_json_from_menu(self.esc_menu_elements[j]))

        temp_menu_dict[f"esc_menu"] = esc_menu_list

        with open(output, "w", encoding = "utf-8") as f:
            json.dump(temp_menu_dict, f, indent = 4)
        
        print(f"menuer gemt til fil {output}")


    def afslut(self):
        self.running = False

    def update(self):
        self.menus[self.active_menu].update()
        for i in range (len(self.HUD_elements)):
            self.HUD_elements[i].update()
    
    def draw(self, screen):
        self.menus[self.active_menu].draw(screen)
        for i in range (len(self.HUD_elements)):
            self.HUD_elements[i].draw(screen)

    def esc_update(self):
        self.esc_menu_elements[self.active_esc_menu].update()
    
    def esc_draw(self, screen):
        self.esc_menu_elements[self.active_esc_menu].draw(screen)

    def load_menus(self, json_filename : "str"):

        with open(json_filename, "r", encoding = "utf-8") as f:
            menus = json.load(f)

        for i in range(len(menus["screen_boxes"])):
            self.menus.append(create_menu_from_list(menus["screen_boxes"], i, self.function_map))

        for j in range(len(menus["esc_menu"])):
            self.esc_menu_elements.append(create_menu_from_list(menus["esc_menu"], j, self.function_map))

        for k in range(len(menus["hud"])):
            self.HUD_elements.append(create_menu_from_list(menus["hud"], k, self.function_map))
        print("Menuer indlæst")

    def menu_event_handling(self, event):
        self.menus[self.active_menu].event_handler(event)

        for i in range (len(self.HUD_elements)):
            self.HUD_elements[i].event_handler(event)

    def esc_event_handling(self, event):
        self.esc_menu_elements[self.active_esc_menu].event_handler(event)

def create_menu_from_list(json_data : dict, menu_index : int, function_map : dict = {}) -> screen_box:

    json_data = json_data[menu_index]

    placement_info = UI_component_placement_info(
        json_data["placement_info"][0],
        json_data["placement_info"][1],
        json_data["placement_info"][2],
        json_data["placement_info"][3],
        json_data["placement_info"][4],
        json_data["placement_info"][5]
        )
    color_info = UI_component_color_info(
        (json_data["color_info"][0], json_data["color_info"][1], json_data["color_info"][2]),
        (json_data["color_info"][3], json_data["color_info"][4], json_data["color_info"][5]),
        (json_data["color_info"][6], json_data["color_info"][7], json_data["color_info"][8])
    )
    if "border" in json_data:
        border = json_data["border"]
    else:
        border = 8

    menu = screen_box(placement_info, color_info, border)

    for index in range(len(json_data["components"])):

        index_component = json_data["components"][index]
        component_color = UI_component_color_info()
        component_placement = UI_component_placement_info(0, 0, 0, 0, "Askeslaske", "Askeslaske")
        component_text = ""
        component_text_size = 20

        if  index_component["color_info"] != None:
            component_color = UI_component_color_info(
                (index_component["color_info"][0], index_component["color_info"][1], index_component["color_info"][2]),
                (index_component["color_info"][3], index_component["color_info"][4], index_component["color_info"][5]),
                (index_component["color_info"][6], index_component["color_info"][7], index_component["color_info"][8])
            )
        else:
            component_color = None
        if index_component["placement_info"] != None:
            component_placement = UI_component_placement_info(
                index_component["placement_info"][0],
                index_component["placement_info"][1],
                index_component["placement_info"][2],
                index_component["placement_info"][3],
                index_component["placement_info"][4],
                index_component["placement_info"][5]
            )
        else:
            component_placement = None

        if index_component["text"] != None:
                component_text = index_component["text"]

        if index_component["text_size"] != None:
            component_text_size = int(index_component["text_size"])

        if index_component["button_function_id"] != None:
            func_key = index_component["button_function_id"]
            ## func_key = local_function_map.get(func_key, None)
        else:
            func_key = None

        menu.create_UIcomponent(component_color, component_placement, component_text, component_text_size, func_key, index_component["visible"], function_map)
    #menus.append(menu)
    return menu

def create_json_from_menu(menu: screen_box) -> dict:
    # --- Grundstruktur ---
    menu_dict = {
        "color_info": [],
        "placement_info": [],
        "components": []
    }

    # --- Farver ---
    color = menu.color_info
    menu_dict["color_info"] = [
        color.primary_color[0], color.primary_color[1], color.primary_color[2],
        color.secondary_color[0], color.secondary_color[1], color.secondary_color[2],
        color.accent_color[0], color.accent_color[1], color.accent_color[2]
    ]

    # --- Placering ---
    menu_dict["placement_info"] = [
        menu.rect.x + menu.rect.width // 2,   # center X
        menu.rect.y + menu.rect.height // 2,  # center Y
        menu.rect.width,
        menu.rect.height,
        "center",
        "center"
    ]

    # --- Komponenter ---
    for comp in menu.components:
        comp_dict = {}

        # Farve
        if comp.color_info != menu.color_info:
            c = comp.color_info
            comp_dict["color_info"] = [
                c.primary_color[0], c.primary_color[1], c.primary_color[2],
                c.secondary_color[0], c.secondary_color[1], c.secondary_color[2],
                c.accent_color[0], c.accent_color[1], c.accent_color[2]
            ]
        else:
            comp_dict["color_info"] = None

        # Synlighed
        comp_dict["visible"] = comp.visible

        # Placering
        if comp.placement_info != None:
            p = comp.placement_info
            comp_dict["placement_info"] = [
                p.x, p.y, p.width, p.height, p.anchor_x, p.anchor_y
            ]
        else:
            comp_dict["placement_info"] = None

        # Tekst
        comp_dict["text"] = comp.text.text
        comp_dict["text_size"] = comp.text.size

        # Knapfunktion
        if isinstance(comp.button, UI_button_extension):
            comp_dict["button_function_id"] = comp.button.function_id
        else:
            comp_dict["button_function_id"] = None

        # Tilføj til listen
        menu_dict["components"].append(comp_dict)

    return menu_dict

"""
def start():
    game.running = True

def afslut():
    game.running = False
    print("skider i bukserne")

def skift_menu():
    game.skift_menu()

def gem_menu():
    game.save_menu_layout("Askeslaske.json")

def flyt():
    game.menus[game.active_menu].move(1300, 600)

def tilføj_knap():
    game.menus[game.active_menu].create_UIcomponent(None, None, "Yay", None, "afslut")

def toggle_esc_menu():
    game.esc_menu = not game.esc_menu

function_map = {
    "afslut": afslut,
    "start": start,
    "intet": intet,
    "skift_menu": skift_menu,
    "flyt" : flyt,
    "tilføj_knap": tilføj_knap,
    "gem_menu" : gem_menu,
    "toggle_esc_menu": toggle_esc_menu,
    "null": None
}

game = Game(function_map)

if __name__ == "__main__":

    #with open("menu.jacob", "w", encoding = "utf-8") as f:
    #    json.dump(main_menu, f, indent = 4)

    with open("menu.json", "r", encoding = "utf-8") as f:
        main_menu = json.load(f)
    
    pygame.init()
    pygame.font.init()

    # Populate menus
    for i in range(len(main_menu["screen_boxes"])):
        game.menus.append(create_menu_from_list(main_menu["screen_boxes"], i, game.function_map))

    for j in range(len(main_menu["esc_menu"])):
        game.esc_menu_elements.append(create_menu_from_list(main_menu["esc_menu"], j, game.function_map))

    #game.HUD_elements.append(create_menu_from_json(main_menu, 1, game.function_map))

    screen = pygame.display.set_mode((1600, 800))

    while game.running == True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game.esc_menu = not game.esc_menu
            
            if game.esc_menu != True:
                game.menus[game.active_menu].event_handler(event)
                #for elements in game.HUD_elements:
                #    game.HUD_elements[elements].event_handler(event)
            else:
                # Opdaterer pausemenuen
                for element in range (len(game.esc_menu_elements)):
                    game.esc_menu_elements[element].event_handler(event)

        if game.esc_menu != False:
            #opdaterer og håndterer pausemenuen.
            for i in range(len(game.esc_menu_elements)):
                game.esc_menu_elements[i].update()
                game.esc_menu_elements[i].draw(screen)
            pygame.display.flip()
            continue

        screen.fill((30, 144, 255))  # Dodger blue
        game.menus[game.active_menu].update()
        game.menus[game.active_menu].draw(screen)

        #for elements in game.HUD_elements:
        #    game.HUD_elements[elements].update()
        #    game.HUD_elements[elements].draw(screen)

        pygame.display.flip()
    pygame.quit()

"""