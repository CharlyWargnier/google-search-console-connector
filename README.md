
#  🎈Google Search Console Streamlit Connector

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://search-console-connector.streamlitapp.com/)

   * ✔️ One-click connect to the [Google Search Console API](https://developers.google.com/webmaster-tools)
   * ✔️ Easily traverse your account hierarchy
   * ✔️ Go beyond the [1K row UI limit](https://www.gsqi.com/marketing-blog/how-to-bulk-export-search-features-from-gsc/)
   * ✔️ Enrich your data querying with multiple dimensions layers and extra filters!

✍️ You can read the blog post [here](https://blog.streamlit.io/p/e89fd54e-e6cd-4e00-8a59-39e87536b260/) for more information.

#### Going beyond the `10K` row limit

   * There's a `10K` row limit per API call on the [Cloud](https://streamlit.io/cloud) version to prevent crashes.
   * You can remove that limit by [forking the app](https://github.com/CharlyWargnier/google-search-console-connector) and adjusting the `RowCap` variable in the `streamlit_app.py` file

#### Kudos

This app relies on Josh Carty's excellent [Search Console Python wrapper](https://github.com/joshcarty/google-searchconsole). Big kudos to him for creating it!

#### Questions, comments, or report a 🐛?

   * If you have any questions or comments, please DM [me](https://twitter.com/DataChaz). Alternatively, you can ask the [Streamlit community](https://discuss.streamlit.io).
   * If you find a bug, please raise an issue in [Github](https://github.com/CharlyWargnier/google-search-console-connector/pulls).

#### Known bugs
   * You can filter any dimension in the table even if the dimension hasn't been pre-selected. I'm working on a fix for this.
  
