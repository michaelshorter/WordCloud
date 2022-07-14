using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.IO.Pipes;


class Program
{

    static string YourSubscriptionKey = "9951ce8cec2d423cb09494b4d2a8b8d7";
    static string YourServiceRegion = "uksouth";

    async static Task Main(string[] args)
    {
        using var pipe = new NamedPipeServerStream("testpipe");
        Console.WriteLine("Waiting for pipe client to connect...");
        pipe.WaitForConnection();
        Console.WriteLine("Pipe client connected.");

        var recognitionEnd = new TaskCompletionSource<string?>();

        var speechConfig = SpeechConfig.FromSubscription(YourSubscriptionKey, YourServiceRegion);
	// Swiss German
        //speechConfig.SpeechRecognitionLanguage = "de-CH";
	// German
        //speechConfig.SpeechRecognitionLanguage = "de-DE";
	// English
        speechConfig.SpeechRecognitionLanguage = "en-US";

        using var audioConfig = AudioConfig.FromDefaultMicrophoneInput();
        using var speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);

        speechConfig.SetProperty(PropertyId.SpeechServiceResponse_PostProcessingOption, "2");

        speechRecognizer.Recognizing += (object? sender, SpeechRecognitionEventArgs e) =>
            {
                if (ResultReason.RecognizingSpeech == e.Result.Reason && e.Result.Text.Length > 0)
                {

                    //Console.Clear();
                    //Console.WriteLine($"{e.Result.Text}");
		            string lastWord = e.Result.Text.Split(' ').Last();
                    Console.WriteLine($"{lastWord}");

                    try 
                    {
                        byte[] messageBytes = Encoding.UTF8.GetBytes(lastWord);
                        pipe.Write(messageBytes, 0, messageBytes.Length);
                        /*
                        using (StreamWriter sw = new StreamWriter(pipe)) 
                        {
                            //var buf = Encoding.ASCII.GetBytes(lastWord);     // Get ASCII byte array     
                            //_bw.Write((uint)buf.Length);                // Write string length
                            //_bw.Write(buf);                              // Write string
                        }*/
                    }
                    catch (IOException err)
                    {
                        Console.WriteLine("PIPE ERROR: {0}", err.Message);
                    }
                }
                else if (ResultReason.NoMatch == e.Result.Reason)
                {
                    Console.WriteLine($"NOMATCH: Speech could not be recognized.{Environment.NewLine}");
                }

            };
        speechRecognizer.Recognized += (object? sender, SpeechRecognitionEventArgs e) =>
            {

                if (ResultReason.RecognizedSpeech == e.Result.Reason && e.Result.Text.Length > 0)
                {

                    //Console.Clear();
                    Console.WriteLine($"Recognized: {e.Result.Text}");
                    using (StreamWriter sw = new StreamWriter("content.txt", true)) 
                    {
                        sw.BaseStream.Seek(0, SeekOrigin.End);
                        sw.WriteLine($"{e.Result.Text}");
                    }
                }
                else if (ResultReason.NoMatch == e.Result.Reason)
                {
                    Console.WriteLine($"NOMATCH: Speech could not be recognized.{Environment.NewLine}");
                }
            };

        speechRecognizer.Canceled += (object? sender, SpeechRecognitionCanceledEventArgs e) =>
            {
                if (CancellationReason.EndOfStream == e.Reason)
                {
                    Console.WriteLine($"End of stream reached.{Environment.NewLine}");
                    recognitionEnd.TrySetResult(null); 
                }
                else if (CancellationReason.CancelledByUser == e.Reason)
                {
                    Console.WriteLine($"User canceled request.{Environment.NewLine}");
                    recognitionEnd.TrySetResult(null); 
                }
                else if (CancellationReason.Error == e.Reason)
                {
                    var error = $"Encountered error.{Environment.NewLine}Error code: {(int)e.ErrorCode}{Environment.NewLine}Error details: {e.ErrorDetails}{Environment.NewLine}";
                    Console.WriteLine($"{error}");
                    recognitionEnd.TrySetResult(error); 
                }
                else
                {
                    var error = $"Request was cancelled for an unrecognized reason: {(int)e.Reason}.{Environment.NewLine}";
                    Console.WriteLine($"{error}");
                    recognitionEnd.TrySetResult(error); 
                }
            };

        speechRecognizer.SessionStopped += (object? sender, SessionEventArgs e) =>
            {
                
                Console.WriteLine($"Session stopped.{Environment.NewLine}");
                recognitionEnd.TrySetResult(null); 
            };

        Console.WriteLine($"Ready");
        await speechRecognizer.StartContinuousRecognitionAsync().ConfigureAwait(false);
        Console.WriteLine($"Speak");
        // Waits for recognition end.
        Task.WaitAll(new[] { recognitionEnd.Task });

        // Stops recognition.
        await speechRecognizer.StopContinuousRecognitionAsync().ConfigureAwait(false);

        return ;
    }
}
