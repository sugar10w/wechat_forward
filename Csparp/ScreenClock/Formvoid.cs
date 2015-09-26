using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ScreenClock
{
    public partial class Formvoid : Form
    {
        public delegate void TCPEventHandler(object sender, TcpEventArgs e);
        public TCPEventHandler tcpEvent = new TCPEventHandler(TCPhandler);

        public Formvoid()
        {
            InitializeComponent();
            
        }

        static public void TCPhandler(object sender, TcpEventArgs e)
        {
            if (e.data == "撒花")
            {
                for (int i = 0; i < 10; ++i)
                    new FormClock(e.data).Show();
            }
            else
            {
                FormClock bb = new FormClock(e.data);
                bb.Show();
            }
        }

        private void Formvoid_Load(object sender, EventArgs e)
        {
            TcpEvent tcp = new TcpEvent(this);
        }
    }
}
