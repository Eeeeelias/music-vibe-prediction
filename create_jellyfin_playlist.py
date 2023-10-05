from datetime import datetime


def read_tsv(file):
    with open(file, "r", encoding='utf-8') as f:
        data = f.readlines()
    data = [line.strip().split("\t") for line in data]
    return data


def get_pathlist(data):
    pathlist = []
    genres = set()
    duration = 0
    for row in data:
        fixed_path = row[1].replace('P:', '/media').replace('\\', '/').replace('&', '&amp;')
        item = f"  <PlaylistItem>\n      <Path>{fixed_path}</Path>\n    </PlaylistItem>"
        pathlist.append(item)
        genres.add(f"<Genre>{row[2]}</Genre>")
        duration += int(row[3])
    return pathlist, genres, duration


def create_xml(pathlist, genres, duration):
    xml = f"""<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<Item>
  <Added>{datetime.now().strftime("%m/%d/%Y %H:%M:%S")}</Added>
  <LockData>false</LockData>
  <LocalTitle>Calming Music</LocalTitle>
  <RunningTime>{duration // 60}</RunningTime>
  <Genres>
"""
    for genre in genres:
        xml += f"    {genre}\n"
    xml += "  </Genres>\n"
    xml += "  <PlaylistItems>\n"
    for item in pathlist:
        xml += f"  {item}\n"
    xml += "  </PlaylistItems>\n"

    xml += """  <Shares>
    <Share>
      <UserId>a0740c9c79af4fb3876ccce20d835cbc</UserId>
      <CanEdit>true</CanEdit>
    </Share>
  </Shares>
  <PlaylistMediaType>Audio</PlaylistMediaType>
</Item>"""
    return xml


if __name__ == '__main__':
    data = read_tsv("cluster6.tsv")
    pathlist, genres, duration = get_pathlist(data)
    xml = create_xml(pathlist, genres, duration)
    with open("calming_music.xml", "w", encoding='utf-8') as f:
        f.write(xml)