using System;
using System.Collections;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static AutoApproval.AdminHistory.Data;

namespace AutoApproval.AdminHistory
{
    public interface IDataExtractor
    {
        List<Data> GetData();
        List<Data> GetDataToBeReviewed();
    }

    public class DataExtractor: IDataExtractor
    {
        public List<Data> GetData()
        {
            List<Data> data = new List<Data>();
            //TODO: Get data here

            int counter = 0;
            string line;

            // Read the file and display it line by line.
            System.IO.StreamReader file =
               new System.IO.StreamReader(ConfigurationManager.AppSettings["DataFile"]);
            while ((line = file.ReadLine()) != null)
            {
                try
                {
                    String[] content = line.Split('|');
                    String result = content[0];
                    String comment = content[2].Substring(1, content[2].Length - 2);
                    Outcome outcome;
                    Enum.TryParse(result, out outcome);
                    data.Add(new Data { Result = outcome, Text = comment });
                }
                catch(Exception ex)
                {
                    Console.WriteLine("Something failed "+ex.ToString());
                }
            }

            file.Close();

            return data;
        }

        public List<Data> GetDataToBeReviewed()
        {
            List<Data> data = new List<Data>();
            //TODO: Get data here

            int counter = 0;
            string line;

            // Read the file and display it line by line.
            System.IO.StreamReader file =
               new System.IO.StreamReader(ConfigurationManager.AppSettings["DataToBeReviewedFile"]);
            while ((line = file.ReadLine()) != null)
            {
                data.Add(new Data { Text = line });
            }

            file.Close();

            return data;
        }
    }
}
