@register(outgoing=True, pattern=r"^.movie (.*)")
async def movie(movent):
    title = movent.pattern_match.group(1)
    url = "https://api.gdriveplayer.us/"
    res = get(url + "v1/movie/search", params={"title": title})
    if res.text != 'null':
        imdb = []
        for x in res.json():
            a = x["imdb"]
            imdb.append(a)
        data = []
        for y in imdb:
            b = get(url + "v1/imdb/" + y).json()
            text = (
                f"**{b['Title']}**\n\n"
                f"**Rating:** {b['imdbRating']}\n"
                f"**Genre:** {b['Genre']}\n"
                f"**Production:** {b['Production']}\n"
                f"**Released:** {b['Released']}\n"
                f"**[WATCH]({b['player_url']})**"
            )
            poster = b["Poster"]
            data.append({"text": text, "poster": poster})
        for z in data:
            r = get(z["poster"], stream=True)
            r.raw.decode_content = True
            poster = Image.open(r.raw)
            poster.thumbnail((360, 360), Image.ANTIALIAS)
            poster.save("poster.jpg", "JPEG")
            await movent.client.send_file(
                movent.chat_id,
                "poster.jpg",
                caption=z["text"],
                parse_mode="Markdown",
            )
            os.remove("poster.jpg")
    else:
	    await movent.edit("No result found")
