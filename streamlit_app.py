import streamlit as st
import pandas as pd

# imports for search console libraries
import searchconsole
from apiclient import discovery
from google_auth_oauthlib.flow import Flow

# imports for streamlit elements
from streamlit_elements import Elements

# from streamlit_elements import elements, sync, event

# imports for aggrid
from st_aggrid import AgGrid
from st_aggrid import AgGrid
import pandas as pd
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from st_aggrid import GridUpdateMode, DataReturnMode

# from os import error
import os

# The code below is for the layout of the page
if "widen" not in st.session_state:
    layout = "centered"
else:
    layout = "wide" if st.session_state.widen else "centered"

st.set_page_config(
    layout=layout, page_title="Google Search Console Connector", page_icon="🎈"
)

# row limit
RowCap = 10000

tab1, tab2, tab3 = st.tabs(["Main", "To-do's", "⚙️ Limitations"])

with tab2:

    with st.expander("To-do"):

        st.write(
            """
    * Finish explanation in aggrid tips section
    * Fix alignment of rows in the filter section convo: https://snowflake.slack.com/archives/C03AFAHCG1J/p1658239877172969
    * Finish explanation in the "about" section
    * Check that "You can't see pages and pages" error message is triggered properly
    * From requests.exceptions import ReadTimeout except ReadTimeout: # Try the same request again (https://kite.trade/forum/discussion/10941/socket-timeout-the-read-operation-timed-out)
        
        """
        )

        st.write("")

    with st.expander("Optional"):

        st.write(
            """
    * [Design] add a right arrow at the top (make your selection)
    * [Design] remove all the hashed code in the file
    * [Design] add a gif when loading?
        
        """
        )

        st.write("")

    with st.expander("Done"):

        st.write(
            """

    * [Design] check that "log in first" message is correct
    * Add switch to toggle between "centered" and "wide" layout
    * Adding a little tick box when connection is ok
    * [Done, by duplicating the forms] Remove containers as it seems to be creating a bug?
    * [Done] Add thousands separator to the number of results
    * Add a 2nd nested dimension, and make sure it is working properly
    * [Karen] Remove token print at the top of the page (hashed "st.write(st.session_state.my_token_input)")
    * [AgGrid] increase AGGrid size OF THE GRID
    * [AgGrid] [ASKED ON TWITTER] add index to aggrid
    * Display the number of rows in the table (see Twitter app)
    * Add remaining dimensions to the app (device, country, etc)
    * Add a message about 10k rows limit
    * In Arrow image, change "select a course" with "You need to log in via Google OAuth first. Log in via left hand side menu!"
    * [Design] add an expander "about this connector"
    * add a download button when native table is selected
    * [Design] add "app created" message
    * Remove colored emojis as it looks too much!
    * Fix checkbox AgGrid bug: Aggrid table is displayed even if checkbox is unchecked
    * Fix checkbox AgGrid bug: sometimes 2 aggrid tables are displayed
    * Try to deploy with new secrets (it's working locally)
    * Change formatting on Aggrid tips (make it like proper mardown (see Diffcheker or DBT readme))
    * [AgGrid] Add a text on how to download the data in aggrid
    * move JSON credentials to a TOML file
    * remove aggrid table at the top of the page
    * [Design] remove duplicated dataframe
    * replace 'fetch data' by 'access API data'
    * Try to deploy the app to streamlit cloud
    * remove fileExists = os.path.isfile("data.csv") and see if it works
    * [AgGrid] add option to switch between aggrid and table
    * add exception handling for ValueError: Please supply either code or authorization_response parameters
    * add search console logo
    * remove check all properties in the account
    * remove dafault "Web property to review"
    * add exception handling for discover data (when no data is returned)
    * Update aggrid as red highlight issue now
    * remove the non aggrid dataframe
    * try site_list to get a list of sites
    * DONE -> Update service account credentials to remove streamprophet (https://console.cloud.google.com/apis/credentials/consent?project=ultra-envoy-290208)

        
        """
        )
        st.write("")

st.markdown("")

st.sidebar.image("logo.png", width=290)

st.sidebar.markdown("")

st.write("")

with tab3:

    st.write(
        """
* 10K rows limit on the Cloud version
* If you have more data, you can fork the app and remove the row limit
* You can filter any dimension in the table even if the dimension hasn't been added pre-selected. I'm working on a fix for this.
    
    """
    )

    st.write("")


with tab1:

    # Convert secrets from the TOML file to strings
    clientSecret = str(st.secrets["installed"]["client_secret"])
    clientId = str(st.secrets["installed"]["client_id"])

    st.markdown("")

    if "my_token_input" not in st.session_state:
        st.session_state["my_token_input"] = ""

    if "my_token_received" not in st.session_state:
        st.session_state["my_token_received"] = False

    def charly_form_callback():
        # st.write(st.session_state.my_token_input)
        st.session_state.my_token_received = True

    with st.sidebar.form(key="my_form"):

        st.markdown("")

        mt = Elements()

        mt.button(
            "Sign-in with Google",
            target="_blank",
            size="large",
            variant="contained",
            start_icon=mt.icons.exit_to_app,
            onclick="none",
            style={"color": "#FFFFFF", "background": "#FF4B4B"},
            href="https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=686079794781-0bt8ot3ie81iii7i17far5vj4s0p20t7.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fwebmasters.readonly&state=vryYlMrqKikWGlFVwqhnMpfqr1HMiq&prompt=consent&access_type=offline",
        )

        mt.show(key="687")

        credentials = {
            "installed": {
                "client_id": clientId,
                "client_secret": clientSecret,
                "redirect_uris": [],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
            }
        }

        flow = Flow.from_client_config(
            credentials,
            # st.secrets["installed"],
            scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
            redirect_uri="urn:ietf:wg:oauth:2.0:oob",
        )

        auth_url, _ = flow.authorization_url(prompt="consent")

        code = st.text_input(
            "Google Oauth token",
            key="my_token_input",
            help="Please sign in to your account via Google OAuth, then paste your OAuth token in the field below.",
            type="password",
        )

        submit_button = st.form_submit_button(
            label="Access GSC API", on_click=charly_form_callback
        )

        st.write("")

    container3 = st.sidebar.container()

    st.sidebar.write("")

    with st.sidebar.expander("About this app"):

        st.write(
            """
    Say good riddance to the Google Search Console 1,000 row limit! 👋

    This mighty app connects to your Google Search Console profiles in one click and gets you **ALL** the data you need!
        
        """
        )

        st.write("")

    st.sidebar.write("")

    st.sidebar.caption(
        "Made in 🎈 [Streamlit](https://www.streamlit.io/), by [Charly Wargnier](https://www.charlywargnier.com/)."
    )

    try:

        if st.session_state.my_token_received == False:

            with st.form(key="my_form2"):

                # text_input_container = st.empty()
                webpropertiesNEW = st.text_input(
                    "Web property to review (please sign in via Google OAuth first)",
                    value="",
                    disabled=True,
                )

                filename = webpropertiesNEW.replace("https://www.", "")
                filename = filename.replace("http://www.", "")
                filename = filename.replace(".", "")
                filename = filename.replace("/", "")

                col1, col2, col3 = st.columns(3)

                with col1:
                    dimension = st.selectbox(
                        "Dimension",
                        (
                            "query",
                            "page",
                            "date",
                            "device",
                            "searchAppearance",
                            "country",
                        ),
                        help="the dimension to analyze",
                    )

                with col2:
                    nested_dimension = st.selectbox(
                        "Nested dimension",
                        (
                            "none",
                            "query",
                            "page",
                            "date",
                            "device",
                            "searchAppearance",
                            "country",
                        ),
                        help="you can expand  your analysis by adding a nested dimension",
                    )

                with col3:
                    nested_dimension_2 = st.selectbox(
                        "Nested dimension 2",
                        (
                            "none",
                            "query",
                            "page",
                            "date",
                            "device",
                            "searchAppearance",
                            "country",
                        ),
                        help="you can expand  your analysis even more by adding a second nested dimension!",
                    )

                st.write("")

                col1, col2 = st.columns(2)

                with col1:
                    search_type = st.selectbox(
                        "Search type",
                        ("web", "discover", "news", "video", "googleNews", "image"),
                        help="You can specify the search type data you want to retrieve by using the search_type method with your query. The following values are currently supported by the API: news, video, image, web, discover & googleNews. If you don't use this method, the default value used will be web,",
                    )

                with col2:
                    timescale = st.selectbox(
                        "Date range",
                        (
                            "Last 7 days",
                            "Last 30 days",
                            "Last 3 months",
                            "Last 6 months",
                            "Last 12 months",
                            "Last 16 months",
                        ),
                        index=0,
                        help="You can specify the date range you want to retrieve by using the timescale method with your query. The following values are currently supported by the API: Last 7 days, Last 30 days, Last 3 months, Last 6 months, Last 12 months, Last 16 months. If you don't use this method, the default value used will be Last 7 days",
                    )

                    if timescale == "Last 7 days":
                        timescale = -7
                    elif timescale == "Last 30 days":
                        timescale = -30
                    elif timescale == "Last 3 months":
                        timescale = -91
                    elif timescale == "Last 6 months":
                        timescale = -182
                    elif timescale == "Last 12 months":
                        timescale = -365
                    elif timescale == "Last 16 months":
                        timescale = -486

                st.write("")

                with st.expander("Filters", expanded=True):

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        filter_page_or_query = st.selectbox(
                            "Dimension to filter (#1)",
                            ("query", "page", "device", "searchAppearance", "country"),
                            help="You can specify the filter type you want to use by using the filter_type method with your query. The following values are currently supported by the API: page, query. If you don't use this method, the default value used will be page,",
                        )

                    with col2:
                        filter_type = st.selectbox(
                            "Filter type",
                            (
                                "contains",
                                "equals",
                                "notContains",
                                "notEquals",
                                "includingRegex",
                                "excludingRegex",
                            ),
                            help="Note that if you use Regex in your filter, you must follow RE2 syntax.",
                        )

                    with col3:
                        filter_keyword = st.text_input(
                            "Keyword(s) to filter ",
                            "",
                            help="Add the keyword(s) you want to filter",
                        )

                    with col1:
                        filter_page_or_query2 = st.selectbox(
                            "Dimension to filter (#2)",
                            ("query", "page", "device", "searchAppearance", "country"),
                            key="filter_page_or_query2",
                            help="You can specify the filter type you want to use by using the filter_type method with your query. The following values are currently supported by the API: page, query. If you don't use this method, the default value used will be page,",
                        )

                    with col2:
                        filter_type2 = st.selectbox(
                            "Filter type",
                            (
                                "contains",
                                "equals",
                                "notContains",
                                "notEquals",
                                "includingRegex",
                                "excludingRegex",
                            ),
                            key="filter_type2",
                            help="Note that if you use Regex in your filter, you must follow RE2 syntax.",
                        )

                    with col3:
                        filter_keyword2 = st.text_input(
                            "Keyword(s) to filter ",
                            "",
                            key="filter_keyword2",
                            help="Add the keyword(s) you want to filter",
                        )

                    with col1:
                        filter_page_or_query3 = st.selectbox(
                            "Dimension to filter (#3)",
                            ("query", "page", "device", "searchAppearance", "country"),
                            key="filter_page_or_query3",
                            help="You can specify the filter type you want to use by using the filter_type method with your query. The following values are currently supported by the API: page, query. If you don't use this method, the default value used will be page,",
                        )

                    with col2:
                        filter_type3 = st.selectbox(
                            "Filter type",
                            (
                                "contains",
                                "equals",
                                "notContains",
                                "notEquals",
                                "includingRegex",
                                "excludingRegex",
                            ),
                            key="filter_type3",
                            help="Note that if you use Regex in your filter, you must follow RE2 syntax.",
                        )

                    with col3:
                        filter_keyword3 = st.text_input(
                            "Keyword(s) to filter ",
                            "",
                            key="filter_keyword3",
                            help="Add the keyword(s) you want to filter",
                        )

                    st.write("")

                submit_button = st.form_submit_button(
                    label="Fetch GSC API data", on_click=charly_form_callback
                )

            if (nested_dimension != "none") and (nested_dimension_2 != "none"):

                if (
                    (dimension == nested_dimension)
                    or (dimension == nested_dimension_2)
                    or (nested_dimension == nested_dimension_2)
                ):
                    st.warning(
                        "🚨 Dimension and nested dimensions cannot be the same, please make sure you choose unique dimensions."
                    )
                    st.stop()

                else:
                    pass

            elif (nested_dimension != "none") and (nested_dimension_2 == "none"):
                if dimension == nested_dimension:
                    st.warning(
                        "🚨 Dimension and nested dimensions cannot be the same, please make sure you choose unique dimensions."
                    )
                    st.stop()
                else:
                    pass

            else:
                pass

        if st.session_state.my_token_received == True:

            @st.experimental_singleton
            def get_account_site_list_and_webproperty(token):
                flow.fetch_token(code=token)
                credentials = flow.credentials
                service = discovery.build(
                    serviceName="webmasters",
                    version="v3",
                    credentials=credentials,
                    cache_discovery=False,
                )

                account = searchconsole.account.Account(service, credentials)
                site_list = service.sites().list().execute()
                # webproperty = account[webpropertiesNEW]
                return account, site_list

            account, site_list = get_account_site_list_and_webproperty(
                st.session_state.my_token_input
            )

            first_value = list(site_list.values())[0]

            lst = []
            for dicts in first_value:
                a = dicts.get("siteUrl")
                lst.append(a)

            if lst:

                container3.info("✔️ GSC credentials OK!")

                with st.form(key="my_form2"):

                    webpropertiesNEW = st.selectbox("Select web property", lst)

                    # filename = webpropertiesNEW.replace("https://www.", "")
                    # filename = filename.replace("http://www.", "")
                    # filename = filename.replace(".", "")
                    # filename = filename.replace("/", "")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        dimension = st.selectbox(
                            "Dimension",
                            (
                                "query",
                                "page",
                                "date",
                                "device",
                                "searchAppearance",
                                "country",
                            ),
                            help="the dimension to analyze",
                        )

                    with col2:
                        nested_dimension = st.selectbox(
                            "Nested dimension",
                            (
                                "none",
                                "query",
                                "page",
                                "date",
                                "device",
                                "searchAppearance",
                                "country",
                            ),
                            help="you can expand  your analysis by adding a nested dimension",
                        )

                    with col3:
                        nested_dimension_2 = st.selectbox(
                            "Nested dimension 2",
                            (
                                "none",
                                "query",
                                "page",
                                "date",
                                "device",
                                "searchAppearance",
                                "country",
                            ),
                            help="you can expand  your analysis even more by adding a second nested dimension!",
                        )

                    st.write("")

                    col1, col2 = st.columns(2)

                    with col1:
                        search_type = st.selectbox(
                            "Search type",
                            ("web", "discover", "news", "video", "googleNews", "image"),
                            help="You can specify the search type data you want to retrieve by using the search_type method with your query. The following values are currently supported by the API: news, video, image, web, discover & googleNews. If you don't use this method, the default value used will be web,",
                        )

                    with col2:
                        timescale = st.selectbox(
                            "Date range",
                            (
                                "Last 7 days",
                                "Last 30 days",
                                "Last 3 months",
                                "Last 6 months",
                                "Last 12 months",
                                "Last 16 months",
                            ),
                            index=0,
                            help="You can specify the date range you want to retrieve by using the timescale method with your query. The following values are currently supported by the API: Last 7 days, Last 30 days, Last 3 months, Last 6 months, Last 12 months, Last 16 months. If you don't use this method, the default value used will be Last 7 days",
                        )

                        if timescale == "Last 7 days":
                            timescale = -7
                        elif timescale == "Last 30 days":
                            timescale = -30
                        elif timescale == "Last 3 months":
                            timescale = -91
                        elif timescale == "Last 6 months":
                            timescale = -182
                        elif timescale == "Last 12 months":
                            timescale = -365
                        elif timescale == "Last 16 months":
                            timescale = -486

                    st.write("")

                    with st.expander("💎 Filters", expanded=True):

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            filter_page_or_query = st.selectbox(
                                "Dimension to filter (#1)",
                                (
                                    "query",
                                    "page",
                                    "device",
                                    "searchAppearance",
                                    "country",
                                ),
                                help="You can specify the filter type you want to use by using the filter_type method with your query. The following values are currently supported by the API: page, query. If you don't use this method, the default value used will be page,",
                            )

                        with col2:
                            filter_type = st.selectbox(
                                "Filter type",
                                (
                                    "contains",
                                    "equals",
                                    "notContains",
                                    "notEquals",
                                    "includingRegex",
                                    "excludingRegex",
                                ),
                                help="Note that if you use Regex in your filter, you must follow RE2 syntax.",
                            )

                        with col3:
                            filter_keyword = st.text_input(
                                "Keyword(s) to filter ",
                                "",
                                help="You can specify the keyword(s) you want to filter by using the filter_keyword method with your query. If you don't use this method, the default value used will be empty,",
                            )

                        with col1:
                            filter_page_or_query2 = st.selectbox(
                                "Dimension to filter (#2)",
                                (
                                    "query",
                                    "page",
                                    "device",
                                    "searchAppearance",
                                    "country",
                                ),
                                key="filter_page_or_query2",
                                help="You can specify the filter type you want to use by using the filter_type method with your query. The following values are currently supported by the API: page, query. If you don't use this method, the default value used will be page,",
                            )

                        with col2:
                            filter_type2 = st.selectbox(
                                "Filter type",
                                (
                                    "contains",
                                    "equals",
                                    "notContains",
                                    "notEquals",
                                    "includingRegex",
                                    "excludingRegex",
                                ),
                                key="filter_type2",
                                help="Note that if you use Regex in your filter, you must follow RE2 syntax.",
                            )

                        with col3:
                            filter_keyword2 = st.text_input(
                                "Keyword(s) to filter ",
                                "",
                                key="filter_keyword2",
                                help="You can specify the keyword(s) you want to filter by using the filter_keyword method with your query. If you don't use this method, the default value used will be empty,",
                            )

                        with col1:
                            filter_page_or_query3 = st.selectbox(
                                "Dimension to filter (#3)",
                                (
                                    "query",
                                    "page",
                                    "device",
                                    "searchAppearance",
                                    "country",
                                ),
                                key="filter_page_or_query3",
                                help="You can specify the filter type you want to use by using the filter_type method with your query. The following values are currently supported by the API: page, query. If you don't use this method, the default value used will be page,",
                            )

                        with col2:
                            filter_type3 = st.selectbox(
                                "Filter type",
                                (
                                    "contains",
                                    "equals",
                                    "notContains",
                                    "notEquals",
                                    "includingRegex",
                                    "excludingRegex",
                                ),
                                key="filter_type3",
                                help="Note that if you use Regex in your filter, you must follow RE2 syntax.",
                            )

                        with col3:
                            filter_keyword3 = st.text_input(
                                "Keyword(s) to filter ",
                                "",
                                key="filter_keyword3",
                                help="You can specify the keyword(s) you want to filter by using the filter_keyword method with your query. If you don't use this method, the default value used will be empty,",
                            )

                        st.write("")

                    submit_button = st.form_submit_button(
                        label="Fetch GSC API data", on_click=charly_form_callback
                    )

                if (nested_dimension != "none") and (nested_dimension_2 != "none"):

                    if (
                        (dimension == nested_dimension)
                        or (dimension == nested_dimension_2)
                        or (nested_dimension == nested_dimension_2)
                    ):
                        st.warning(
                            "🚨 Dimension and nested dimensions cannot be the same, please make sure you choose unique dimensions."
                        )
                        st.stop()

                    else:
                        pass

                elif (nested_dimension != "none") and (nested_dimension_2 == "none"):
                    if dimension == nested_dimension:
                        st.warning(
                            "🚨 Dimension and nested dimensions cannot be the same, please make sure you choose unique dimensions."
                        )
                        st.stop()
                    else:
                        pass

                else:
                    pass

            # form.slider("Inside the form")
            # form.form_submit_button("Submit")
            # def get_search_console_data(webproperty, days=-720):

            def get_search_console_data(webproperty):
                if webproperty is not None:
                    # query = webproperty.query.range(start="today", days=days).dimension("query")
                    report = (
                        webproperty.query.search_type(search_type)
                        .range("today", days=timescale)
                        .dimension(dimension)
                        .filter(filter_page_or_query, filter_keyword, filter_type)
                        .filter(filter_page_or_query2, filter_keyword2, filter_type2)
                        .filter(filter_page_or_query3, filter_keyword3, filter_type3)
                        .limit(RowCap)
                        .get()
                        .to_dataframe()
                    )
                    # report
                    # df = pd.DataFrame(r.rows)
                    return report
                else:
                    st.warning("No webproperty found")
                    st.stop()

            def get_search_console_data_nested(webproperty):
                if webproperty is not None:
                    # query = webproperty.query.range(start="today", days=days).dimension("query")
                    report = (
                        webproperty.query.search_type(search_type)
                        .range("today", days=timescale)
                        .dimension(dimension, nested_dimension)
                        .filter(filter_page_or_query, filter_keyword, filter_type)
                        .filter(filter_page_or_query2, filter_keyword2, filter_type2)
                        .filter(filter_page_or_query3, filter_keyword3, filter_type3)
                        .limit(RowCap)
                        .get()
                        .to_dataframe()
                    )
                    return report

            def get_search_console_data_nested_2(webproperty):
                if webproperty is not None:
                    # query = webproperty.query.range(start="today", days=days).dimension("query")
                    report = (
                        webproperty.query.search_type(search_type)
                        .range("today", days=timescale)
                        .dimension(dimension, nested_dimension, nested_dimension_2)
                        .filter(filter_page_or_query, filter_keyword, filter_type)
                        .filter(filter_page_or_query2, filter_keyword2, filter_type2)
                        .filter(filter_page_or_query3, filter_keyword3, filter_type3)
                        .limit(RowCap)
                        .get()
                        .to_dataframe()
                    )
                    return report

            # some conditions to check which function to call

            if nested_dimension == "none" and nested_dimension_2 == "none":

                webproperty = account[webpropertiesNEW]

                df = get_search_console_data(webproperty)

                if df.empty:
                    st.warning(
                        "🚨 There's no data for your selection, please refine your search with different criteria"
                    )
                    st.stop()

            elif nested_dimension_2 == "none":

                webproperty = account[webpropertiesNEW]

                df = get_search_console_data_nested(webproperty)

                if df.empty:
                    st.warning(
                        "🚨 DataFrame is empty! Please refine your search with different criteria"
                    )
                    st.stop()

            else:

                webproperty = account[webpropertiesNEW]

                df = get_search_console_data_nested_2(webproperty)

                if df.empty:
                    st.warning(
                        "🚨 DataFrame is empty! Please refine your search with different criteria"
                    )
                    st.stop()

            st.write("")

            st.write(
                "##### This API call has returned ",
                # len(df.index),
                f"{len(df.index):,}" " rows. The beta is capped at ",
                str(int(RowCap / 1000)) + "k",
                " rows. More soon!",
            )

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                # st.selectbox("Layout", ["centered", "wide"], key="layout", help="You can change the layout to either centered or wide.")
                st.caption("")
                check_box = st.checkbox(
                    "💥 Ag-Grid mode!", help="Tick this box to see the data in Ag-grid!"
                )
                st.caption("")

            with col2:
                st.caption("")
                st.checkbox(
                    "Widen layout",
                    key="widen",
                    help="Tick this box to change the layout to 'wide' mode",
                )
                st.caption("")

            if not check_box:

                st.dataframe(df, height=500)

                @st.cache
                def convert_df(df):
                    # IMPORTANT: Cache the conversion to prevent computation on every rerun
                    return df.to_csv().encode("utf-8")

                csv = convert_df(df)  #

                st.caption("")

                st.download_button(
                    label="Download table as CSV",
                    data=csv,
                    file_name="large_df.csv",
                    mime="text/csv",
                )

            elif check_box:

                df = df.reset_index()

                gb = GridOptionsBuilder.from_dataframe(df)
                # enables pivoting on all columns, however i'd need to change ag grid to allow export of pivoted/grouped data, however it select/filters groups
                gb.configure_default_column(
                    enablePivot=True, enableValue=True, enableRowGroup=True
                )
                gb.configure_selection(selection_mode="multiple", use_checkbox=True)
                gb.configure_side_bar()  # side_bar is clearly a typo :) should by sidebar
                gridOptions = gb.build()

                with st.expander("💡 Ag-grid tips", expanded=False):

                    st.markdown(
                        """
    #### Easy export!

    You can export your fitlered dataframe to CSV, Excel, as follows:

    ```bash
    >> place your mouse on the grid and right click on it
    >> select "Export to CSV"

    ```

    #### Selecting rows

    Tip! Hold the shift key when selecting rows to select multiple rows at once!


    #### Pivot tables in Ag-grid

    You can export your fitlered dataframe to CSV, Excel, as follows:

    ```bash
    >> place your mouse on the grid and right click on it
    >> select "Export to CSV"

    ```
                    )"""
                    )

                    st.success(
                        f"""
                            🎈 Tip! Hold the shift key when selecting rows to select multiple rows at once!
                            """
                    )

                response = AgGrid(
                    df,
                    gridOptions=gridOptions,
                    enable_enterprise_modules=True,
                    update_mode=GridUpdateMode.MODEL_CHANGED,
                    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
                    height=1000,
                    fit_columns_on_grid_load=True,
                    configure_side_bar=True,
                )
                # df = pd.DataFrame(response["selected_rows"])

    except ValueError as ve:

        # container.info(
        #     "👈 You need to log in via Google OAuth first. Log in via left hand side menu!"
        # )

        # emoji_backhand_index = container.image("Arrow2.png", width=700)
        #
        # col1, col2 = st.columns([1,3])
        #
        # with col1:
        #     emoji_backhand_index3 = container.image("https://emojipedia-us.s3.amazonaws.com/source/skype/289/left-arrow_2b05-fe0f.png", width=40)
        #
        # with col2:
        #     st.sidebar.warning("You need to log in via Google OAuth first. Log in via left hand side menu!")
        #     # container3 = st.container()

        st.warning(
            "You need to log in via Google OAuth first. Log in via left hand side menu!"
        )
