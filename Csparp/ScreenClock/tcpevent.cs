using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace ScreenClock
{
    public class TcpEventArgs : EventArgs
    {
        public const string InializeError = "服务器连接初始化错误。";
        public const string ConnectSuccess = "服务器已连接。";
        public const string WaitingError = "服务器已断开。";

        public string data;
    }

    class TcpEvent
    {
        public Formvoid Father;
        const int port = 12352;
        const string host = "101.200.189.136";
       // const string host = "127.0.0.1";
        Socket soc;

        public TcpEvent(Formvoid father)
        {
            Father = father;

            ConnectServer();

            if (soc == null) return;

            Thread t = new Thread(recvData);
            t.IsBackground = true;
            t.Start();
        }

        public void CallFather(string s)
        {
            if (Father != null)
            {
                TcpEventArgs e = new TcpEventArgs();
                e.data = s;
                Father.BeginInvoke(Father.tcpEvent, this, e);
            }
        }

        public void ConnectServer()
        {
            IPAddress ip = IPAddress.Parse(host);
            IPEndPoint ipe = new IPEndPoint(ip, port);

            soc = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            try
            {
                soc.Connect(ipe);
                soc.Send(Encoding.UTF8.GetBytes("asta2015"));
            }
            catch (SocketException ex)
            {
                CallFather(TcpEventArgs.InializeError);
                return;
            }

            CallFather(TcpEventArgs.ConnectSuccess);

        }

        public void recvData()
        {

            while (true)
            {
                byte[] result = new byte[1024];
                int receiveLength = 0;

                try
                {
                    if (soc != null) receiveLength = soc.Receive(result);
                    else throw new SocketException();
                }
                catch (SocketException ex)
                {
                    CallFather(TcpEventArgs.WaitingError);
                    return;
                }

                string s = Encoding.UTF8.GetString(result, 0, receiveLength);
                CallFather(s);

            }

            
            //IPEndPoint ip = new IPEndPoint(IPAddress.Any, 5068);
            //Socket newsock = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
            //newsock.Bind(ip);

            //IPEndPoint sender_s = new IPEndPoint(IPAddress.Any, 0);

            //while (true)
            //{
            //    TcpEventArgs e = new TcpEventArgs();
            //    e.data = new byte[1024];
            //    EndPoint Remote = (EndPoint)(sender_s);
            //    e.data = new byte[4096];
            //    //发送接受信息
            //    e.recv = newsock.ReceiveFrom(e.data, ref Remote);
            //    if (Father != null)
            //    {
            //        Father.BeginInvoke(Father.tcpEvent, this, e);
                    
            //    }
            //}
        }

    }
}
