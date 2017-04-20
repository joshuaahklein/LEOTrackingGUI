using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Timers;
using System.Windows.Forms; 

namespace LEOTrackingGUI
{
    public partial class Form1 : Form
    {
        private int status = 0; //0 = Not tracking, 1 = tracking

        public GPSDialog gpsDialog = new GPSDialog();
        public TLEDialog tleDialog = new TLEDialog();

        private string GPSlatitude;
        private string GPSlongitude;
        private string TLE;

        private System.Timers.Timer myTimer;

        private string python, satApp, planeApp, basePath;
        private ProcessStartInfo psi;
        private Process pyScript;
        private static StreamReader reader; 
        private static string pyOutStr = "1";

        public Form1()
        {
            InitializeComponent();

            //Remove bin\Debug for base path
            Console.WriteLine(Directory.GetCurrentDirectory());
            string path = Directory.GetCurrentDirectory();
            basePath = path.Substring(0, path.Length - @"LEOTrackingGUI\bin\Debug".Length);
            python = basePath + @"Python\Shell\python.exe";
            satApp = basePath + @"Python\SatTracking\pathpredict.py";
            planeApp = basePath + @"Python\PlaneTracking\script.py";

            //Set default values
            TLE = "1 25544U 98067A   17041.55333126  .00016717  00000-0  10270-3 0  9008" + "\n" 
                + "2 25544  51.6430 309.5978 0006847 175.5696 184.5519 15.54335653  2056";
            tleLabel.Text = "TLE: " + TLE;
            gpsLabel.Text = "GPS Coordinates\nLatitude: 0.00\nLongitude: 0.00";
            GPSlatitude = GPSlongitude = "0.00";
            tleDialog.TLE = TLE;

            //Set up timer
            myTimer = new System.Timers.Timer();
            myTimer.Elapsed += new ElapsedEventHandler(DisplayTimeEvent);
            myTimer.Interval = 1000; // 1000 ms is one second
            myTimer.Enabled = true;
        }

        //Timer handler, for periodically getting data from py scripts
        public static void DisplayTimeEvent(object source, ElapsedEventArgs e)
        {
            //Read output from process
            //pyOutStr = reader.ReadLine();
        }
        
        //Clock handler; also runs functions every second if necessary
        private void timer1_Tick_1(object sender, EventArgs e)
        {
            //Update clock
            clockLabel.Text = ("Current time: "+DateTime.Now.ToString("HH:mm:ss"));

            //Update current position field
            if (status == 1)
            {
                currentPositionLabel.Text = "Current Position: " + pyOutStr + ".";
            }
            else currentPositionLabel.Text = "Not tracking.";
            
            Invalidate();
        }

        //Handler for new GPS entry
        private void gPSCoordinateToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //Set given default
            gpsDialog.GPSlat = GPSlatitude;
            gpsDialog.GPSlong = GPSlongitude;

            //Write result
            if (gpsDialog.ShowDialog() == DialogResult.OK)
            {
                GPSlatitude = gpsDialog.GPSlat;
                GPSlongitude = gpsDialog.GPSlong;
                gpsLabel.Text = "GPS Coordinates\nLatitude: "+GPSlatitude+"\nLongitude: "+GPSlongitude;
                Invalidate();
            }
        }

        //Handler for new TLE entry
        private void tLEToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (tleDialog.ShowDialog() == DialogResult.OK)
            {
                TLE = tleDialog.TLE;
                tleLabel.Text = "TLE: "+TLE;
                Invalidate();
            }
        }

        //Load video file on startup -- will need to change to processed image file later
        //Also used to start python scripts
        private void Form1_Load(object sender, EventArgs e)
        {
            //axWindowsMediaPlayer1.URL = @"C:\Users\Joshua\Desktop\LEOTrackingGUI\Sat_225122_08232016.mp4";
            //axWindowsMediaPlayer2.URL = @"C:\Users\Joshua\Desktop\LEOTrackingGUI\Sat_235411_08232016.mp4";
            //axWindowsMediaPlayer1.Ctlcontrols.stop();
            //axWindowsMediaPlayer2.Ctlcontrols.stop();
        }

        private void trackingButton_Click(object sender, EventArgs e)
        {
            //Error handling
            if (status == 1)
            {
                MessageBox.Show("Already tracking object.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            if (TLE == null || TLE == "")
            {
                MessageBox.Show("Invalid TLE data.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            if (GPSlatitude == null || GPSlongitude == null || GPSlatitude == "" || GPSlongitude == "")
            {
                MessageBox.Show("Invalid GPS data.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            //Run python script, load streams, set status
            status = 1;
            axWindowsMediaPlayer1.Ctlcontrols.play();
            axWindowsMediaPlayer2.Ctlcontrols.play();

            //Set up process for running py script, read from stdout
            string app = (radioTLE.Checked) ? satApp : planeApp;
            psi = new ProcessStartInfo(python, app);
            psi.UseShellExecute = false;
            psi.RedirectStandardOutput = true;

            //Pass arguments
            psi.Arguments = app + " " + GPSlatitude + " " + GPSlongitude + 
                " \"" + TLE + "\" ";
            
            //Start process
            pyScript = new Process();
            pyScript.StartInfo = psi;
            pyScript.Start();

            reader = pyScript.StandardOutput;
            pyOutStr = reader.ReadToEnd();

            //Run OpenCV .exe

            Process.Start(basePath+@"\SatelliteTracker\x64\Debug\SatelliteTracker.exe");





         
            pyScript.WaitForExit();
            pyScript.Close();
            status = 0;


            Console.WriteLine(pyOutStr);
        }

        private void abortButton_Click(object sender, EventArgs e)
        {
            //Error handling
            if (status == 0)
            {
                MessageBox.Show("Not tracking any objects.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            //Stop streams, set status,
            //WILL NEED TO ADD KILL COMMAND HERE WHEN INTERFACED WITH MOTOR DRIVERS
            status = 0;
            axWindowsMediaPlayer1.Ctlcontrols.stop();
            axWindowsMediaPlayer2.Ctlcontrols.stop();
        }
    }
}