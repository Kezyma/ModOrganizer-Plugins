using Newtonsoft.Json;
using System.Text.RegularExpressions;

namespace MetaGenerator
{
    internal class Program
    {
        public static string FileIdRegex = $"file_id=(?<fileId>[0-9]*)";
        public class Plugin
        {
            public string PluginId { get; set; }
            public string GameId { get; set; }
            public int NexusId { get; set; }
            public string MO2Game { get; set; }
        }

        static void Main(string[] args)
        {
            var json = Path.GetFullPath("Plugins.json");
            var dest = Path.GetFullPath("Meta");
            if (!Directory.Exists(dest)) Directory.CreateDirectory(dest);
            if (File.Exists(json))
            {
                Console.WriteLine("Reading Plugins.json");
                var text = File.ReadAllText(json);
                var plugins = JsonConvert.DeserializeObject<List<Plugin>>(text);
                foreach (var plugin in plugins)
                {
                    Console.WriteLine($"Generating meta file for {plugin.PluginId}");
                    using var client = new HttpClient();
                    var res = client.GetAsync($"https://www.nexusmods.com/{plugin.GameId}/mods/{plugin.NexusId}?tab=files").Result;
                    var html = res.Content.ReadAsStringAsync().Result;
                    var match = Regex.Match(html, FileIdRegex);
                    var fileId = match.Groups["fileId"].Value;
                    var metaString = $"[General]\ninstalled=true\ngameName={plugin.MO2Game}\nmodID={plugin.NexusId}\nfileID={fileId}";
                    File.WriteAllText(Path.Combine(dest, $"{plugin.PluginId}.meta"), metaString);
                }
            }
        }
    }

    
}
