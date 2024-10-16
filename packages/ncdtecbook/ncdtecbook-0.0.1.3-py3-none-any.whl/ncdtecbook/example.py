import ipywidgets as widgets
from IPython.display import display

# stack = Stack()



def stack_vis_example(stack):
    btn = widgets.Button(description="Show stack")
    btn.on_click(lambda b: StackDisplay(stack).show()  )
    display(btn)
    

class StackDisplay():
    def __init__(self, stack):
        self.stack = stack


        # Create text to display the stack
        self.stack_display = widgets.Text(
            value="",
            placeholder="Stack state",
            description="Stack:",
            disabled=True
        )
        # Create text area to display result of stack operation
        self.stack_log = widgets.Textarea(
            value="",
            placeholder="Operation result",
            description="Output:",
            layout=widgets.Layout(width="500px", height="100px"),
            disabled=True
        )

        # Button to push item
        self.push_input = widgets.Text(
            value='',
            placeholder='Enter item',
            description='Item:',
            disabled=False
        )
        
        self.push_button = widgets.Button(
            description="Push",
            button_style='success',
        )



        self.pop_button = widgets.Button(
            description="Pop",
            button_style='danger',
        )
        
        self.peek_button = widgets.Button(
            description="Peek",
            button_style='info',
        )
       
        self.clear_button = widgets.Button(
            description="Clear output",
            button_style='warning'
        )



    # Function to update the stack display
    def update_display(self):
        self.stack_display.value = f"{self.stack.stack[::-1]}"



    def push_item(self,b):
        if self.push_input.value:
            value = self.push_input.value      
            self.stack.push(value)
            self.push_input.value = ''
            self.stack_log.value += f"\nPushed: {value}"

            self.update_display()


    # Button to pop item
    def pop_item(self,b):
        popped = self.stack.pop()
        self.stack_log.value += f"\nPopped: {popped}"
        self.update_display()

    # Button to peek item
    def peek_item(self,b):
        top = self.stack.peek()
        self.stack_log.value += f"\nPeeked: {top}"


    def clear_display(self,b):
        self.stack_log.value = ""
    
    def show(self):



        self.push_button.on_click(self.push_item)

        self.pop_button.on_click(self.pop_item)



        self.peek_button.on_click(self.peek_item)
        self.clear_button.on_click(self.clear_display)

    
        # Layout the buttons and stack display
        buttons = widgets.HBox([self.push_button, self.pop_button, self.peek_button])
        display(self.push_input, buttons, self.stack_display, self.stack_log, self.clear_button)