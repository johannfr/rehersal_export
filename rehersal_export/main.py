from pydub import AudioSegment
import click
from glob import glob
from pathlib import Path
import re
import sys

NB_HAVE = "~/Nextcloud/Naboens Have/Øvelokale/date/session"


@click.command()
@click.argument("input_dir", type=click.Path(exists=True, dir_okay=True))
@click.argument(
    "output_dir", type=click.Path(dir_okay=True), required=False, default=NB_HAVE
)
def main(input_dir, output_dir):
    input_dir = Path(input_dir)

    session_name, year, month, day = re.search(
        "(\w+)-(\d{4})-(\d{2})-(\d{2})", input_dir.name
    ).groups()

    takes = []
    print(f"Exporting audio files from {input_dir}")

    audiofiles_path = input_dir / f"interchange/{input_dir.name}/audiofiles"

    all_files = sorted(glob(str(audiofiles_path / "*.wav")))

    le_match = re.search(r"Take(\d+)_Audio (\d+)-", all_files[-1])
    takes = int(le_match.group(1))
    tracks = int(le_match.group(2))

    output_dir = Path(
        output_dir.replace("date", f"{year}-{month}-{day}").replace(
            "session", session_name
        )
    ).expanduser()
    print(f"Exporting to {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    for take in range(1, takes + 1):
        print(f"Exporting take {take} of {takes}...")
        drums_left = AudioSegment.from_file(
            audiofiles_path / f"Take{take}_Audio 1-1.wav"
        )
        drums_right = AudioSegment.from_file(
            audiofiles_path / f"Take{take}_Audio 2-1.wav"
        )
        stereo_drums = AudioSegment.from_mono_audiosegments(drums_left, drums_right)

        for track in range(3, tracks + 1):
            print(f"\tMixing track {track} of {tracks}...")
            next_segment = AudioSegment.from_file(
                audiofiles_path / f"Take{take}_Audio {track}-1.wav", channels=1
            )
            stereo_drums = stereo_drums.overlay(next_segment)
        stereo_drums.export(output_dir / f"Take{take}_Mixed.mp4", format="mp4")
    print("Exporting stems...")
    for file in [Path(f) for f in all_files]:
        print(f"\t{file.name}")
        AudioSegment.from_file(file).export(
            str(output_dir / Path(file).name).replace(".wav", ".mp4"), format="mp4"
        )


if __name__ == "__main__":
    main()
