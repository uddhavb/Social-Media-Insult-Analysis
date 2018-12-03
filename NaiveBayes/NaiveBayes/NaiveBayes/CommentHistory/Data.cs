using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AutoApproval.AdminHistory
{
    public class Data
    {
        public enum Outcome
        {
            Insult,
            NotAnInsult
        }
        public Outcome Result { get; set; }
        public String Text { get; set; }
    }
}
