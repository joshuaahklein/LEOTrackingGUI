namespace LEOTrackingGUI
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.menuStrip2 = new System.Windows.Forms.MenuStrip();
            this.fileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.newToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.gPSCoordinateToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.tLEToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.clockLabel = new System.Windows.Forms.Label();
            this.gpsLabel = new System.Windows.Forms.Label();
            this.tleLabel = new System.Windows.Forms.Label();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.currentPositionLabel = new System.Windows.Forms.Label();
            this.trackingButton = new System.Windows.Forms.Button();
            this.abortButton = new System.Windows.Forms.Button();
            this.radioTLE = new System.Windows.Forms.RadioButton();
            this.radioPlanes = new System.Windows.Forms.RadioButton();
            this.menuStrip2.SuspendLayout();
            this.SuspendLayout();
            // 
            // menuStrip1
            // 
            this.menuStrip1.Location = new System.Drawing.Point(0, 24);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(1236, 24);
            this.menuStrip1.TabIndex = 0;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // menuStrip2
            // 
            this.menuStrip2.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fileToolStripMenuItem});
            this.menuStrip2.Location = new System.Drawing.Point(0, 0);
            this.menuStrip2.Name = "menuStrip2";
            this.menuStrip2.Size = new System.Drawing.Size(1236, 24);
            this.menuStrip2.TabIndex = 1;
            this.menuStrip2.Text = "menuStrip2";
            // 
            // fileToolStripMenuItem
            // 
            this.fileToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.newToolStripMenuItem});
            this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            this.fileToolStripMenuItem.Size = new System.Drawing.Size(37, 20);
            this.fileToolStripMenuItem.Text = "File";
            // 
            // newToolStripMenuItem
            // 
            this.newToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.gPSCoordinateToolStripMenuItem,
            this.tLEToolStripMenuItem});
            this.newToolStripMenuItem.Name = "newToolStripMenuItem";
            this.newToolStripMenuItem.Size = new System.Drawing.Size(98, 22);
            this.newToolStripMenuItem.Text = "New";
            // 
            // gPSCoordinateToolStripMenuItem
            // 
            this.gPSCoordinateToolStripMenuItem.Name = "gPSCoordinateToolStripMenuItem";
            this.gPSCoordinateToolStripMenuItem.Size = new System.Drawing.Size(157, 22);
            this.gPSCoordinateToolStripMenuItem.Text = "GPS Coordinate";
            this.gPSCoordinateToolStripMenuItem.Click += new System.EventHandler(this.gPSCoordinateToolStripMenuItem_Click);
            // 
            // tLEToolStripMenuItem
            // 
            this.tLEToolStripMenuItem.Name = "tLEToolStripMenuItem";
            this.tLEToolStripMenuItem.Size = new System.Drawing.Size(157, 22);
            this.tLEToolStripMenuItem.Text = "TLE";
            this.tLEToolStripMenuItem.Click += new System.EventHandler(this.tLEToolStripMenuItem_Click);
            // 
            // clockLabel
            // 
            this.clockLabel.AutoSize = true;
            this.clockLabel.Location = new System.Drawing.Point(12, 35);
            this.clockLabel.Name = "clockLabel";
            this.clockLabel.Size = new System.Drawing.Size(34, 13);
            this.clockLabel.TabIndex = 2;
            this.clockLabel.Text = "Clock";
            // 
            // gpsLabel
            // 
            this.gpsLabel.AutoSize = true;
            this.gpsLabel.Location = new System.Drawing.Point(138, 35);
            this.gpsLabel.Name = "gpsLabel";
            this.gpsLabel.Size = new System.Drawing.Size(88, 13);
            this.gpsLabel.TabIndex = 3;
            this.gpsLabel.Text = "GPS Coordinates";
            // 
            // tleLabel
            // 
            this.tleLabel.AutoSize = true;
            this.tleLabel.Location = new System.Drawing.Point(268, 35);
            this.tleLabel.Name = "tleLabel";
            this.tleLabel.Size = new System.Drawing.Size(27, 13);
            this.tleLabel.TabIndex = 4;
            this.tleLabel.Text = "TLE";
            // 
            // timer1
            // 
            this.timer1.Enabled = true;
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick_1);
            // 
            // currentPositionLabel
            // 
            this.currentPositionLabel.AutoSize = true;
            this.currentPositionLabel.Location = new System.Drawing.Point(12, 626);
            this.currentPositionLabel.Name = "currentPositionLabel";
            this.currentPositionLabel.Size = new System.Drawing.Size(81, 13);
            this.currentPositionLabel.TabIndex = 6;
            this.currentPositionLabel.Text = "Current Position";
            // 
            // trackingButton
            // 
            this.trackingButton.Location = new System.Drawing.Point(1019, 35);
            this.trackingButton.Name = "trackingButton";
            this.trackingButton.Size = new System.Drawing.Size(98, 23);
            this.trackingButton.TabIndex = 8;
            this.trackingButton.Text = "Start Tracking";
            this.trackingButton.UseVisualStyleBackColor = true;
            this.trackingButton.Click += new System.EventHandler(this.trackingButton_Click);
            // 
            // abortButton
            // 
            this.abortButton.Location = new System.Drawing.Point(1123, 35);
            this.abortButton.Name = "abortButton";
            this.abortButton.Size = new System.Drawing.Size(101, 23);
            this.abortButton.TabIndex = 9;
            this.abortButton.Text = "Abort Tracking";
            this.abortButton.UseVisualStyleBackColor = true;
            this.abortButton.Click += new System.EventHandler(this.abortButton_Click);
            // 
            // radioTLE
            // 
            this.radioTLE.AutoSize = true;
            this.radioTLE.Checked = true;
            this.radioTLE.Location = new System.Drawing.Point(843, 41);
            this.radioTLE.Name = "radioTLE";
            this.radioTLE.Size = new System.Drawing.Size(76, 17);
            this.radioTLE.TabIndex = 10;
            this.radioTLE.TabStop = true;
            this.radioTLE.Text = "Track TLE";
            this.radioTLE.UseVisualStyleBackColor = true;
            // 
            // radioPlanes
            // 
            this.radioPlanes.AutoSize = true;
            this.radioPlanes.Location = new System.Drawing.Point(925, 41);
            this.radioPlanes.Name = "radioPlanes";
            this.radioPlanes.Size = new System.Drawing.Size(88, 17);
            this.radioPlanes.TabIndex = 11;
            this.radioPlanes.Text = "Track Planes";
            this.radioPlanes.UseVisualStyleBackColor = true;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1236, 176);
            this.Controls.Add(this.radioPlanes);
            this.Controls.Add(this.radioTLE);
            this.Controls.Add(this.abortButton);
            this.Controls.Add(this.trackingButton);
            this.Controls.Add(this.currentPositionLabel);
            this.Controls.Add(this.tleLabel);
            this.Controls.Add(this.gpsLabel);
            this.Controls.Add(this.clockLabel);
            this.Controls.Add(this.menuStrip1);
            this.Controls.Add(this.menuStrip2);
            this.MainMenuStrip = this.menuStrip1;
            this.Name = "Form1";
            this.Text = "Team LEO Tracking Application";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.menuStrip2.ResumeLayout(false);
            this.menuStrip2.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.MenuStrip menuStrip2;
        private System.Windows.Forms.ToolStripMenuItem fileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem newToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem gPSCoordinateToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem tLEToolStripMenuItem;
        private System.Windows.Forms.Label clockLabel;
        private System.Windows.Forms.Label gpsLabel;
        private System.Windows.Forms.Label tleLabel;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.Label currentPositionLabel;
        private System.Windows.Forms.Button trackingButton;
        private System.Windows.Forms.Button abortButton;
        private System.Windows.Forms.RadioButton radioTLE;
        private System.Windows.Forms.RadioButton radioPlanes;
    }
}

