# def rotaryCallback(self, direction):
#     if self.noisebox.current_meters is None:
#         self.oled_menu.counter
#         if direction == 1:
#             self.oled_menu.counter += 1
#         else:
#             self.oled_menu.counter -= 1
#         self.oled_menu.draw_menu()
#
#
# def switchCallback(self):
#     if self.noisebox.switch_function:
#         """Stop running jacktrip session"""
#
#         self.noisebox.switch_function()
#         self.oled_menu.draw_menu()
#         self.noisebox.switch_function = None
#         return
#
#     if self.noisebox.current_meters:
#         self.noisebox.stop_monitoring_audio()
#         self.oled_menu.draw_menu()
#         return
#
#     strval = self.oled_menu.menu_items[self.oled_menu.menuindex]
#     self.oled_menu.menu_operation(strval)
