import entities

class DisplayScreens():

    def __init__(self, display):

        self.display = display

        # Define the display
        self.menu_display = entities.MAIN_DISPLAY_FORMATTING
        self.line_height = self.menu_display[0]
        self.menu_rows = self.menu_display[1]
        self.x_offset = self.menu_display[2]
        self.highlight_row = self.menu_display[3]

    def welcome_screen(self):
        line_y = 0
        self.display.fill(0)
        for i in range(len(entities.SPLASH_SCREEN)):
            self.display.text(entities.SPLASH_SCREEN[i], self.x_offset, line_y)
            line_y += self.line_height
        self.display.show()
    
    def get_menu_items(self, direction):
        # direction is passed in as a boolean

        # format of sub_list is {0:7, 1:8, 2:0, 3:1, 4:2}
        sub_list = tuple(range(0, len(self.routines)))
        imenu_items_doubled = sub_list + sub_list

        sub_list = {}

        # print(direction)
        start = self.menu_top + 1
        if direction:
            start = self.menu_top - 1

        for i in range (self.menu_rows):
            sub_list[i] = imenu_items_doubled[start]
            start += 1

        # print(sub_list)
        self.menu_top = sub_list[0]

        return sub_list

    def get_menu(self, direction):

        line_y = 0
        menu_items = self.get_menu_items(direction)

        # self.display.rect(0, 24, 128, 15, 1) # eliminate hard coding
        highlight = entities.MENU_HIGHLIGHT
        self.display.rect(highlight[0], highlight[1], highlight[2], highlight[3], highlight[4])

        for i in range (self.menu_rows):
            menu_item = self.routines[menu_items[i]]
            display_item = getattr(entities, menu_item, 'DAY')['name']
            self.display.text(display_item, self.x_offset, line_y)
            line_y += self.line_height

            self.highlighted_item = menu_items[self.highlight_row]

        return self.display