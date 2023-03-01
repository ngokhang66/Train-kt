
using AE.Net.Mail;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;
using SeleniumExtras.WaitHelpers;
using System.Net.Http;
using System.Drawing;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using static System.Windows.Forms.VisualStyles.VisualStyleElement.ListView;
namespace CreateKtem
{

    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            
        }

        private void button1_Click(object sender, EventArgs e)
        {

            string email = "ritavn2lbessie@outlook.com";
            string pwd = "tove3tObj";
            string emailT = "bhy32994@nezid.com";
            string randomPwd = pwd + "@A1";
            
            
            #region Chrome
            string folderPath = @"C:\Users\Kang\PycharmProjects\MultiSelen\";
            string driverPath = "chromedriver1.exe";
            ChromeDriverService service = ChromeDriverService.CreateDefaultService(folderPath, driverPath);
            //hide driver Console? true/false 
            service.HideCommandPromptWindow = true;

            ChromeOptions options = new ChromeOptions();

            //options.BinaryLocation = folderPath + @"GoogleChromePortable1\GoogleChromePortable1.exe";
            options.AddArgument("--user-data-dir=" + folderPath + @"GoogleChromePortable1\Data\profile\");
            options.AddArgument("--profile-directory=" + "Profile 0");
            options.AddExtension(@"C:\Users\Kang\Documents\CSharpDotNet\CreateKtem\anticaptcha-plugin_v0.63.crx");
            options.AddArgument("--disable-blink-features=AutomationControlled");
            options.AddArgument("--render-process-limit=1");
            options.AddArgument("--disable-gpu");
            options.AddArgument("--window-size=600,900");

            ChromeDriver chromeDriver = new ChromeDriver(service, options);

            chromeDriver.Url = "https://howkteam.vn/account/register";
            //chromeDriver.Url = "https://google.com";
            chromeDriver.Navigate();

            try
            {
                 //Mail.Verify(email, pwd, "imap-mail.outlook.com", 993);
                chromeDriver.FindElement(By.XPath("//*[@id=\"Email\"]")).SendKeys(email);
                chromeDriver.FindElement(By.XPath("//*[@id=\"UserName\"]")).SendKeys(email);
                chromeDriver.FindElement(By.XPath("//*[@id=\"Password\"]")).SendKeys(randomPwd);
                chromeDriver.FindElement(By.XPath("//*[@id=\"ConfirmPassword\"]")).SendKeys(randomPwd);
                var submited = chromeDriver.FindElement(By.XPath("/html/body/div/div/div/div/div[1]/h4"), 120);
                Assert.AreEqual("Thông báo", submited.Text);
                bool load = false;
                while (load != true)
                {
                    if (submited.Text == "Thông báo")
                    {
                        Mail.Verify(email, pwd, "imap-mail.outlook.com", 993);
                        load = true;
                    }
                    else
                    {
                        load = false;
                    }
                }

                chromeDriver.Url = "https://howkteam.vn/account/login";
                chromeDriver.Navigate();
                chromeDriver.FindElement(By.XPath("//*[@id=\"Email\"]")).SendKeys(email);
                chromeDriver.FindElement(By.XPath("//*[@id=\"Password\"]")).SendKeys(randomPwd);
                chromeDriver.FindElement(By.XPath("//*[@id=\"loginForm\"]/fieldset/div[4]/button")).Click();
                chromeDriver.Quit();
                
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }

            #endregion

        }

    }

    public static class WebDriverExtensions
    {
        public static IWebElement FindElement(this IWebDriver driver, By by, int timeoutInSeconds)
        {
            if (timeoutInSeconds > 0)
            {
                var wait = new WebDriverWait(driver, TimeSpan.FromSeconds(timeoutInSeconds));
                return wait.Until(ExpectedConditions.ElementIsVisible(by));
            }
            return driver.FindElement(by);
        }
    }

    public static class Mail
    {

        private static readonly HttpClient rq = new HttpClient();
        

        public static void Verify(string email, string pass, string ipmap, int port)
        {
            string url = null;
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
            using (ImapClient ic = new ImapClient())
            {
                ic.Connect(ipmap, port, true, false);
                ic.Login(email, pass);
                ic.SelectMailbox("INBOX");
                int mailcount;
                for (mailcount = ic.GetMessageCount(); mailcount < 2; mailcount = ic.GetMessageCount())
                {
                    Mail.Delay(15);
                    ic.SelectMailbox("INBOX");
                }
                MailMessage[] mm = ic.GetMessages(mailcount - 1, mailcount - 1, false, false);
                MailMessage[] array = mm;
                for (int j = 0; j < array.Length; j++)
                {
                    MailMessage i = array[j];
                    //bool flag = i.Subject == "Account registration confirmation" || i.Subject.Contains("Please verify your account");
                    //if (flag)
                    {
                        string sbody = i.Body;
                        url = Regex.Match(i.Body, "a href=\"(https:[^\"]+)").Groups[1].Value;
                        bool flag2 = string.IsNullOrEmpty(url);
                        if (flag2)
                        {
                            url = Regex.Match(i.Body, "(http.*)").Groups[1].Value.Trim();
                            url = url.Substring(0, url.IndexOf('"'));
                        }
                        break;
                    }
                }
                ic.Dispose();
                
            }
            //return url;

            bool Load = false;
            while (Load != true)
            {
                if (url != null)
                {
                    url = url.Replace("amp;", "&");
                    try
                    {
                        rq.DefaultRequestHeaders.UserAgent.ParseAdd("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36");
                        rq.GetAsync(url);
                        Load = true;
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show(ex.Message);
                    }
                }
                else
                {
                    Load = false;
                }
            }
        }
        private static void Delay(int time)
        {
            for (int i = 0; i < time; i++)
            {
                Thread.Sleep(time);
            }
        }
    }
}