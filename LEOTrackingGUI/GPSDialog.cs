﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace LEOTrackingGUI
{
    public partial class GPSDialog : Form
    {
        public string GPSlat = "0.00";
        public string GPSlong = "0.00";

        public GPSDialog()
        {
            InitializeComponent();

            //Init default values
            gpsTextBox.Text = GPSlat;
            gpsTextBox2.Text = GPSlong;
        }

        private void submitButton_Click(object sender, EventArgs e)
        {
            GPSlat = this.gpsTextBox.Text;
            GPSlong = this.gpsTextBox2.Text;
            DialogResult = DialogResult.OK;
        }

        private void cancelButton_Click(object sender, EventArgs e)
        {
            DialogResult = DialogResult.Cancel;
        }
    }
}
