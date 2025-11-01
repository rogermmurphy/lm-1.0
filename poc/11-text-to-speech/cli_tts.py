"""
POC 11: Simple CLI for Text-to-Speech
Quick and easy command-line interface for Azure TTS.
"""

import sys
import argparse
from azure_tts import AzureTTS


def main():
    parser = argparse.ArgumentParser(
        description="POC 11: Text-to-Speech CLI (Azure)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python cli_tts.py "Hello, world!"
  
  # Specify output file
  python cli_tts.py "Hello, world!" -o greeting.wav
  
  # Use different voice
  python cli_tts.py "Hello, I'm Guy" -v en-US-GuyNeural
  
  # List available voices
  python cli_tts.py --list-voices
  
  # From file
  python cli_tts.py -f script.txt -o narration.wav

Setup:
  Set environment variables:
    AZURE_SPEECH_KEY=your_key
    AZURE_SPEECH_REGION=eastus
        """
    )
    
    parser.add_argument(
        'text',
        nargs='?',
        help='Text to convert to speech'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='output.wav',
        help='Output audio file (default: output.wav)'
    )
    
    parser.add_argument(
        '-v', '--voice',
        default='en-US-JennyNeural',
        help='Voice name (default: en-US-JennyNeural)'
    )
    
    parser.add_argument(
        '-f', '--file',
        help='Read text from file'
    )
    
    parser.add_argument(
        '--list-voices',
        action='store_true',
        help='List all available voices'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize TTS
        tts = AzureTTS(voice=args.voice)
        
        # List voices
        if args.list_voices:
            print("\nAvailable Azure TTS Voices:")
            print("=" * 70)
            voices = tts.list_voices()
            
            # Group by locale
            from collections import defaultdict
            by_locale = defaultdict(list)
            for voice in voices:
                by_locale[voice['locale']].append(voice)
            
            for locale in sorted(by_locale.keys()):
                print(f"\n{locale}:")
                for voice in by_locale[locale]:
                    print(f"  • {voice['name']} ({voice['gender']})")
            
            print(f"\nTotal voices: {len(voices)}")
            return 0
        
        # Get text input
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            print(f"📄 Read {len(text)} characters from {args.file}")
        elif args.text:
            text = args.text
        else:
            parser.print_help()
            return 1
        
        # Convert to speech
        print(f"\n🎙️  Voice: {args.voice}")
        print(f"📝 Text: {text[:100]}{'...' if len(text) > 100 else ''}")
        print(f"💾 Output: {args.output}")
        print(f"\n⏳ Synthesizing...")
        
        success = tts.speak(text, args.output)
        
        if success:
            print(f"\n✅ Success! Audio saved to: {args.output}")
            print(f"💰 Cost: $0 (FREE tier: 500k chars/month)")
            return 0
        else:
            print(f"\n❌ Failed to synthesize speech")
            return 1
            
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nSetup Instructions:")
        print("1. Get Azure Speech API key: https://azure.microsoft.com/services/cognitive-services/speech-services/")
        print("2. Set environment variables:")
        print("   Windows CMD:  set AZURE_SPEECH_KEY=your_key")
        print("   Windows PS:   $env:AZURE_SPEECH_KEY='your_key'")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
