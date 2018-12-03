using NClassifier.Bayesian;
using NRakeCore;
using NRakeCore.StopWordFilters;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AutoApproval.AdminHistory
{
    public class AdminApprovalHistory
    {
        BayesianClassifier Classifier { get; set; }

        public IStopWordFilter StopWordFilter { get; set; }

        public IDataExtractor DataExtractor { get; set; }

        public AdminApprovalHistory(IStopWordFilter stopWordFilter, IDataExtractor dataExtractor)
        {
            IDbConnectionManager odbcConnectionManager = new OdbcConnectionManager(ConfigurationManager.AppSettings["ConnectionString"]);
            IWordsDataSource wordDataSource = new OdbcWordsDataSource(odbcConnectionManager);
            Classifier = new BayesianClassifier(wordDataSource);
            StopWordFilter = stopWordFilter;
            DataExtractor = dataExtractor;
        }

        public bool SaveHistory()
        {
            List<Data> data = DataExtractor.GetData();
            KeywordExtractor k = new KeywordExtractor();
            foreach(var d in data){
                string[] phrases = k.FindKeyPhrases(d.Text);
                string text = string.Join(" ", phrases);
                if (d.Result == Data.Outcome.Insult)
                {
                    Classifier.TeachMatch(Data.Outcome.Insult.ToString(), text);
                    Classifier.TeachNonMatch(Data.Outcome.NotAnInsult.ToString(), text);
                }
                else
                {
                    Classifier.TeachMatch(Data.Outcome.NotAnInsult.ToString(), text);
                    Classifier.TeachNonMatch(Data.Outcome.Insult.ToString(), text);
                }
            }
            return true;
        }

        public void GetOutcomes()
        {
            Console.WriteLine("Starting to test");
            List<Data> data = DataExtractor.GetDataToBeReviewed();
            KeywordExtractor k = new KeywordExtractor();
            foreach (var d in data)
            {
                string[] phrases = k.FindKeyPhrases(d.Text);
                phrases = string.Join(" ", phrases).Split(' ');
                double approved = Classifier.Classify(Data.Outcome.Insult.ToString(), string.Join(" ", phrases).Split(' '));
                double denied = Classifier.Classify(Data.Outcome.NotAnInsult.ToString(), phrases);

                if (approved > 0.7)
                    Console.WriteLine(d.Text +": "+approved +": "+denied +": Insult");
                else if (denied > 0.5)
                    Console.WriteLine(d.Text + ": " + approved + ": " + denied + ": Not an insult");
                else
                    Console.WriteLine(d.Text + ": " + approved + ": " + denied + ": No result");
            }
            Console.Read();
        }
    }
}
