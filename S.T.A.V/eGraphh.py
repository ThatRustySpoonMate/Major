from tkinter import *

#Example Data = [[x,y],[x,y],[x,y],[x,y],[x,y]] #So on...]
#DATA MUST START AT X = 1

class graph:

	def __init__(self, title, xAxisTitle, yAxisTitle, dataSet, master):
		self.master = master
		self.title = title
		self.dataSet = dataSet
		self.dataSet.sort() #Sort data into numerical order of x's
		print(self.dataSet)

		self.flippedData = self.dataSet.copy()

		largestNumTemp = 0
		smallestNumTemp = self.flippedData[0][1]
		for i in range(0, len(self.flippedData) - 1): #Get the largest and smallest numbers in dataset
			if(self.flippedData[i][1] > largestNumTemp):
				largestNumTemp = self.flippedData[i][1]
			if(self.flippedData[i][1] < smallestNumTemp):
				smallestNumTemp = self.flippedData[i][1]

		self.largestNumber = largestNumTemp
		smallestNumber = smallestNumTemp

		#Define scale for plotting point values onto tkinter canvas
		self.yScale = 435 / self.largestNumber
		self.xInterval = 595 / (len(self.flippedData) - 1) 

		
		for i in range(0, len(self.flippedData)): #Flip data over 217.5y vector		
			self.flippedData[i][1] = 435 - self.flippedData[i][1] * self.yScale

			#Convert data co-ordinates into dataPoint objects
			self.flippedData[i] = dataPoint(self.flippedData[i][0], self.flippedData[i][1])


		#print("Max: ", largestNumber,  "\nMin: ",  smallestNumber)


		self.sketch(self.master, xAxisTitle, yAxisTitle)


	def sketch(self, master, xAxisTitle, yAxisTitle):
		#Create new window
		newWindow = Toplevel(master)
		newWindow.geometry("640x480")
		newWindow.title(self.title)
		newWindow.resizable(False, False)

		#Create canvas to draw to
		canvas = Canvas(newWindow)
		#Define axis
		canvas.create_line(40,5,40,440)
		canvas.create_line(40,440,635,440)
		#Label axis
		xAxisText = canvas.create_text(297.5,468, text = xAxisTitle, anchor=CENTER)
		yAxisText = canvas.create_text(7,200, text = yAxisTitle, angle = 90)

		#Draw y-axis gridlines
		for i in range(0, 11):
			canvas.create_line(40, 440 - (43.5 * i), 35,  440 - (43.5 * i))
			canvas.create_text(25, 440 - (43.5 * i), text = str(round(self.largestNumber / 10 * i)), anchor = CENTER) 

		#Draw x-axis gridlines
		for i in range(0, len(self.flippedData)):
			canvas.create_line(40 + self.xInterval * i, 440, 40 + self.xInterval * i,  445)
			canvas.create_text(40 + self.xInterval * i, 455, text = i, anchor = CENTER) 


		#Draw graph
		for i in range(0, len(self.flippedData) - 1):
			canvas.create_line(self.flippedData[i].x * self.xInterval - (self.xInterval - 40), self.flippedData[i].y, self.flippedData[i + 1].x * self.xInterval - (self.xInterval - 40), self.flippedData[i + 1].y)
			#print("X1:",self.flippedData[i].x, "\nY1:", self.flippedData[i].y, "\nX2:",self.flippedData[i + 1].x, "\nY2:", self.flippedData[i + 1].y) #For bugtesting - Will display all points that are being drawn
		canvas.pack(fill=BOTH, expand = 1)


class dataPoint:
	def __init__(self, x, y):
		self.x = x
		self.y = y


