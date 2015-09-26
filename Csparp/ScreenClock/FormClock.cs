using System;
using System.Drawing;
using System.Windows.Forms;
using System.Text;
using System.Collections.Generic;

namespace ScreenClock
{
    public partial class FormClock : Form
    {
        /// <summary>
        /// 表示正在移动窗口
        /// </summary>

        enum MovingType { Common, Flower };
        private MovingType movingType = MovingType.Common;

        private double vHorizonal = 5, vVertical = 0, gravity = 0.1;

        /// <summary>
        /// 用于移动窗口时的坐标换算
        /// </summary>
        
        static public Random ra = new Random();
        static private Color[] clist = 
        { 
            Color.FromArgb(0x66, 0x66, 0x66), 
            Color.FromArgb(0xC1, 0x00, 0x66), 
            Color.FromArgb(0xCC, 0x00, 0x00), 
            Color.FromArgb(0xE6, 0x3F, 0x00), 
            Color.FromArgb(0xEE7700), 
            Color.FromArgb(0xDDAA00), 
            Color.FromArgb(0xEEEE00), 
            Color.FromArgb(0x99DD00), 
            Color.FromArgb(0x66DD00), 
            Color.FromArgb(0x00DD00), 
            Color.FromArgb(0x00DD77), 
            Color.FromArgb(0x00DDAA), 
            Color.FromArgb(0x00DDDD), 
            Color.FromArgb(0x0000CC), 
            Color.FromArgb(0x4400CC), 
            Color.FromArgb(0x5500DD), 
            Color.FromArgb(0x7700BB), 
            Color.FromArgb(0x5500DD), 
            Color.FromArgb(0xA500CC), 
            Color.FromArgb(0xCC00CC), 
        };

        /// <summary>
        /// 设置透明度的对话框
        /// </summary>
        //private Transparency transparency = new Transparency();

        public FormClock(string text)
        {
            InitializeComponent();



            if (text == "撒花")
            {
                movingType = MovingType.Flower;

                labelTime.Width = text.Length * 50;
                this.Size = labelTime.Size;
                this.Width = text.Length * 50;
                labelTime.Text = text;
                labelTime.ForeColor = clist[ra.Next() % 20];

                this.Top = ra.Next() % (Screen.GetWorkingArea(this).Bottom / 4) + Screen.GetWorkingArea(this).Bottom / 2 + this.Height;
                this.Left = Screen.GetWorkingArea(this).Right + ra.Next() % (Screen.GetWorkingArea(this).Right / 2);

                vVertical = - 4 - ra.Next() % 7 ;
                vHorizonal = 7;
            }
            else
            {
                movingType = MovingType.Common;

                labelTime.Width = text.Length * 50;
                this.Size = labelTime.Size;
                this.Width = text.Length * 50;
                labelTime.Text = text;
                labelTime.ForeColor = clist[ra.Next() % 20];

                this.Top = ra.Next() % (Screen.GetWorkingArea(this).Bottom / 4) + this.Height;
                this.Left = Screen.GetWorkingArea(this).Right;

                vHorizonal = 5;
            }
        }

        

        private void timerUpdate_Tick(object sender, EventArgs e)
        {

            switch (movingType)
            {
                case MovingType.Common:
                    this.Left -= (int)vHorizonal;
                    break;
                case MovingType.Flower:

                    vVertical += gravity;
                    this.Top += (int)vVertical;

                    this.Left -= 7;
                    break;
            }

            if (this.Right < Screen.GetWorkingArea(this).Left || this.Top > Screen.GetWorkingArea(this).Bottom)
            {
                this.Close();
            }

        }

        /// <summary>
        /// 不响应Alt+Tab
        /// </summary>
        protected override CreateParams CreateParams
        {
            get
            {
                const int WS_EX_APPWINDOW = 0x40000;
                const int WS_EX_TOOLWINDOW = 0x80;
                CreateParams cp = base.CreateParams;
                cp.ExStyle &= (~WS_EX_APPWINDOW);    // 不显示在TaskBar
                cp.ExStyle |= WS_EX_TOOLWINDOW;      // 不显示在Alt-Tab
                return cp;
            }
        }


    }
}
