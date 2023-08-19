from my_package.model import ImageCaptioningModel
from my_package.model import ImageClassificationModel
from tkinter import *
from functools import partial
from PIL import ImageTk, Image
from tkinter import filedialog


def fileClick(clicked):
    # Define the function you want to call when the filebrowser button (Open) is clicked.
    # This function should pop-up a dialog for the user to select an input image file.
    # To have a better clarity, please check out the sample video.

	imgTypes = [("Image Files", "*.jpg;*.jpeg;*.png")]
	global imgName
	imgName = filedialog.askopenfilename(title = 'Select Image', initialdir = '.\data\imgs', filetypes = imgTypes)
	if imgName:
        # Set the file path to the entry widget.
		e.delete(0, END)
		a = imgName.replace(".\data\imgs", "")
		e.insert(0, a)
	if len(imgName) == 0 : #If no image is selected
		return
	origImg = Image.open(imgName)
	origImg = origImg.resize((500, 500), Image.LANCZOS)
	photoImg = ImageTk.PhotoImage(origImg)
	
	label = Label(root, image=photoImg)
	label.image = photoImg
	label.grid(row=1, column=0, columnspan=4)


def process(clicked, captioner, classifier):
    # This function will produce the required output when 'Process' button is clicked.
    # Note: This should handle the case if the user clicks on the `Process` button without selecting any image file.

    # Catch for No Image Selected
	try : 
		if len(imgName) == 0 :
			print("Choose an image first!")
	except : 
		print("Choose an image first!")
		return
	
	if clicked.get() == "Classification" : # If Classification is choosen from drop-down
		output=classifier(imgName)
		ans = "Top 3 classes:\n\n"
		ans += (output[0][1]+" - " + str(output[0][0]) + "\n"+output[1][1] +
                 " - " + str(output[1][0])+"\n"+output[2][1]+" - " + str(output[2][0]))
		my_Output.config(text=ans)
		print(ans)
		
	else : # If Captioner is choosen from drop-down
		cap = captioner(imgName, 3)
		ans = "Top 3 captions:\n\n"
		ans += (cap[0]+"\n"+cap[1]+"\n"+cap[2])
		my_Output.config(text=ans)
		print(ans)


if __name__ == '__main__':
    # Complete the main function preferably in this order:
    # Instantiate the root window.
    root=Tk()
    # Provide a title to the root window.
    root.title("Image caption generator and Image classifier")
    # Instantiate the captioner, classifier models.
    classifier= ImageClassificationModel()
    captioner=ImageCaptioningModel()

    # Declare the file browsing button.
    options = ["Captioner", "Classification"]
    clicked = StringVar()
    clicked.set(options[0])
    
    e = Entry(root, width=70)
    e.grid(row=0, column=0)

    fileButton = Button(root, text = "Choose img" , command = partial(fileClick,clicked))
    fileButton.grid(row = 0, column = 1)
    # Declare the drop-down button.
    dropDown = OptionMenu(root, clicked, *options)
    dropDown.grid(row = 0, column = 2)
    # Declare the process button.
    myButton = Button(root, text="Process", padx = 10, command=partial(process, clicked, captioner, classifier))
    myButton.grid(row=0, column=3)
    # Declare the output label.
    my_Output = Label(root, text="", relief='solid')
    my_Output.grid(row=1, column=4)
    root.mainloop()
