using System;
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
    public partial class TLEDialog : Form
    {
        public string TLE = "1 25544U 98067A   17041.55333126  .00016717  00000-0  10270-3 0  9008"
            + "\n" + "2 25544  51.6430 309.5978 0006847 175.5696 184.5519 15.54335653  2056";

        public TLEDialog()
        {
            InitializeComponent();

            //Init default values
            tleTextBox.Text = TLE;
        }

        private void submitButton_Click(object sender, EventArgs e)
        {
            TLE = tleTextBox.Text;
            DialogResult = DialogResult.OK;
        }

        private void cancelButton_Click(object sender, EventArgs e)
        {
            DialogResult = DialogResult.Cancel;
        }
    }
}
