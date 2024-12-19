using Hors;

namespace HorstLibrary
{
    public class HorsWrapper
    {
        public string ParseDateTime(string text)
        {
            var parser = new HorsTextParser();

            var result = parser.Parse(text, DateTime.Now);
            return string.Join(", ", result.Dates[0].DateFrom.ToString());
        }

    }
}

