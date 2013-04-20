import processing.serial.*;

//A simple visualisation of the WiichuckInterface output 

Serial wiiChuck;

float newY;
float newRoll;

int TARGET_FRAME_RATE = 60;
float currentFrameRate = 0;

int WIDTH = 400;
int HEIGHT = 600;

int BAT_WIDTH = 20;
int BAT_HEIGHT = 100;


//The range that the paddle is allowed to move within
int HEIGHT_RANGE = 500;

int MIN_Y = (HEIGHT - HEIGHT_RANGE) / 2;
int MAX_Y = HEIGHT - MIN_Y;
int MID_Y = HEIGHT / 2;

//Coordinates relative to centre line
int DRAW_MIN_Y = -250;
int DRAW_MAX_Y = 150;

//offset Wiichuck Y so horizontal Nunchuk gives zero acceleration
int WIICHUCK_ZERO_Y = 69;

//Control sensitivity of input
int WIICHUCK_Y_SENSITIVITY = 50;
float WIICHUCK_ROLL_SENSITIVITY = 1.9;

//The limits of the Wiichuck input
//Actually use slightly within limits so we don't have to strain
// to reach the extremes
int WIICHUCK_MIN_Y = -180 + WIICHUCK_Y_SENSITIVITY;
int WIICHUCK_MAX_Y = 240 - WIICHUCK_Y_SENSITIVITY;

void setup() {
  wiiChuck = new Serial(this, Serial.list()[0], 115200);
  wiiChuck.clear();
  
  frameRate(TARGET_FRAME_RATE);
  
  size(WIDTH, HEIGHT);
  smooth();
}

void draw(){
  drawBackground();
  drawFrameRate();
  drawPaddle(-100);
  drawPaddle(100);
}

void drawBackground() {
  background(255); 
  
  //Draw max, min and centre lines
  stroke(255, 0, 0);
  line(0, HEIGHT / 2, WIDTH, HEIGHT / 2);
  
  stroke(0, 180, 0);
  line(0, MIN_Y, WIDTH, MIN_Y);
  line(0, MAX_Y, WIDTH, MAX_Y);
}

void drawFrameRate() {
  //redraw every 60 frames
  if(frameCount % 60 == 0)
    currentFrameRate = frameRate;
   
   text(String.format("%.0f fps", currentFrameRate), 20, 20);
}

//xOffset is offset from centre
void drawPaddle(int xOffset) {
  noStroke();
  fill(0);
  
  //Translate
  pushMatrix();
  translate(xOffset, getYWiiChuck());
    
  //Rotate
  //Works as planned but is jumpy.
  //TODO: damping/smooth
  pushMatrix();        
  //Move origin to centre of bat
  translate(WIDTH / 2, HEIGHT / 2 + (BAT_HEIGHT / 2));
    
  //Rotate the grid
  rotate(getRollWiiChuck());
    
  //Draw the rect relative to the origin  
  int batLeft = -1 * BAT_WIDTH / 2;
  int batTop = -1 * BAT_HEIGHT / 2;  
  noStroke();
  rect(batLeft, batTop, BAT_WIDTH, BAT_HEIGHT);
  
  //Draw a centre line
  stroke(0, 0, 255);
  line(-30, 0, 30, 0);
  
  popMatrix();
  //End Rotate
    
  popMatrix();
  //End Translate  
}

//Use the Nunchuk's Y acceleration to directly determine the position of the paddle
float getYPositionStyle() {
  float rawY = newY;
  float compensatedY = rawY - WIICHUCK_ZERO_Y;
  float constrainedY = constrain(rawY, WIICHUCK_MIN_Y, WIICHUCK_MAX_Y);
  float mappedY = map(constrainedY, WIICHUCK_MIN_Y, WIICHUCK_MAX_Y, DRAW_MIN_Y, DRAW_MAX_Y);
  
  println(String.format("%.2f,%.2f,%.2f", rawY, compensatedY, constrainedY));
  
  return mappedY;  
}

//Use the Nunchuk's Y acceleration to determine the acceleration of the paddle
float getYAccelerationStyle() {
   //TODO
  return 0; 
}

float getYWiiChuck() {
  return getYPositionStyle();
}

float getRollWiiChuck() {
  return radians(newRoll) * WIICHUCK_ROLL_SENSITIVITY;
}

//Handle WiiChuck serial events
void serialEvent(Serial myPort) {
  String line = wiiChuck.readStringUntil('\n');
  if(line != null) {
    String[] parts = line.split(",");
    if(parts.length == 2) {
      newY = float(parts[1]);
      newRoll = float(parts[0]);
    }
    
  }
  
}
