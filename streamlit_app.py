# basic imports
import streamlit as st
import pandas as pd

# imports for search console libraries
import searchconsole
from apiclient import discovery
from google_auth_oauthlib.flow import Flow

# imports for aggrid
from st_aggrid import AgGrid
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from st_aggrid import GridUpdateMode, DataReturnMode

# all other imports
import os
from streamlit_elements import Elements
import streamlit.components.v1 as components

###############################################################################

# The code below is for the layout of the page
if "widen" not in st.session_state:
    layout = "centered"
else:
    layout = "wide" if st.session_state.widen else "centered"

st.set_page_config(
    layout=layout, page_title="Google Search Console Connector", page_icon="🔌"
)

###############################################################################

# row limit
RowCap = 25000

###############################################################################

_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "my_component",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("my_component", path=build_dir)

def my_component(name, key=None):
    component_value = _component_func(name=name, key=key, default='')
    return component_value

tab1, tab2 = st.tabs(["Main", "About"])

with tab1:

    st.sidebar.image("logo.png", width=290)

    st.sidebar.markdown("")

    st.write("")

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

    oauthtoken = my_component("World")

    with st.sidebar.form(key="my_form"):
        st.session_state["my_token_input"] = oauthtoken

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
            scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
            redirect_uri="urn:ietf:wg:oauth:2.0:oob",
        )

        # auth_url, _ = flow.authorization_url(prompt="consent")

        code = st.text_input(
            "Google Oauth token",
            key="my_token_input",
            help="Sign in to your account via Google OAuth, then paste your OAuth token in the field below.",
            type="password",
        )

        submit_button = st.form_submit_button(
            label="Access GSC API", on_click=charly_form_callback
        )

        st.write("")

    container3 = st.sidebar.container()

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
                        help="Choose a top dimension",
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
                        help="Choose a nested dimension",
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
                        help="Choose a second nested dimension",
                    )

                st.write("")

                col1, col2 = st.columns(2)

                with col1:
                    search_type = st.selectbox(
                        "Search type",
                        ("web", "video", "image", "news", "googleNews"),
                        help="""
                        Specify the search type you want to retrieve
                        -   **Web**: Results that appear in the All tab. This includes any image or video results shown in the All results tab.
                        -   **Image**: Results that appear in the Images search results tab.
                        -   **Video**: Results that appear in the Videos search results tab.
                        -   **News**: Results that show in the News search results tab.

                        """,
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
                        help="Specify the date range",
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

                with st.expander("✨ Advanced Filters", expanded=False):

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        filter_page_or_query = st.selectbox(
                            "Dimension to filter #1",
                            ("query", "page", "device", "searchAppearance", "country"),
                            help="""
                            You can choose to filter dimensions and apply filters before executing a query.
                            """,
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
                            help="""
                            Note that if you use Regex in your filter, you must follow the `RE2` syntax.
                            """,
                        )

                    with col3:
                        filter_keyword = st.text_input(
                            "Keyword(s) to filter ",
                            "",
                            help="Add the keyword(s) you want to filter",
                        )

                    with col1:
                        filter_page_or_query2 = st.selectbox(
                            "Dimension to filter #2",
                            ("query", "page", "device", "searchAppearance", "country"),
                            key="filter_page_or_query2",
                            help="""
                            You can choose to filter dimensions and apply filters before executing a query.
                            """,
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
                            help="""
                            Note that if you use Regex in your filter, you must follow the `RE2` syntax.
                            """,
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
                            "Dimension to filter #3",
                            ("query", "page", "device", "searchAppearance", "country"),
                            key="filter_page_or_query3",
                            help="""
                            You can choose to filter dimensions and apply filters before executing a query.
                            """,
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
                            help="""
                            Note that if you use Regex in your filter, you must follow the `RE2` syntax.
                            """,
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
                            help="Choose your top dimension",
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
                            help="Choose a nested dimension",
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
                            help="Choose a second nested dimension",
                        )

                    st.write("")

                    col1, col2 = st.columns(2)

                    with col1:
                        search_type = st.selectbox(
                            "Search type",
                            ("web", "news", "video", "googleNews", "image"),
                        help="""
                        Specify the search type you want to retrieve
                        -   **Web**: Results that appear in the All tab. This includes any image or video results shown in the All results tab.
                        -   **Image**: Results that appear in the Images search results tab.
                        -   **Video**: Results that appear in the Videos search results tab.
                        -   **News**: Results that show in the News search results tab.

                        """,

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
                            help="Specify the date range",
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

                    with st.expander("✨ Advanced Filters", expanded=False):

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            filter_page_or_query = st.selectbox(
                                "Dimension to filter #1",
                                (
                                    "query",
                                    "page",
                                    "device",
                                    "searchAppearance",
                                    "country",
                                ),
                                help="You can choose to filter dimensions and apply filters before executing a query.",
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
                                help="Note that if you use Regex in your filter, you must follow `RE2` syntax.",
                            )

                        with col3:
                            filter_keyword = st.text_input(
                                "Keyword(s) to filter ",
                                "",
                                help="Add the keyword(s) you want to filter",
                            )

                        with col1:
                            filter_page_or_query2 = st.selectbox(
                                "Dimension to filter #2",
                                (
                                    "query",
                                    "page",
                                    "device",
                                    "searchAppearance",
                                    "country",
                                ),
                                key="filter_page_or_query2",
                                help="You can choose to filter dimensions and apply filters before executing a query.",
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
                                help="Note that if you use Regex in your filter, you must follow `RE2` syntax.",
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
                                "Dimension to filter #3",
                                (
                                    "query",
                                    "page",
                                    "device",
                                    "searchAppearance",
                                    "country",
                                ),
                                key="filter_page_or_query3",
                                help="You can choose to filter dimensions and apply filters before executing a query.",
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
                                help="Note that if you use Regex in your filter, you must follow `RE2` syntax.",
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

            def get_search_console_data(webproperty):
                if webproperty is not None:
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

            # Here are some conditions to check which function to call

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
                "##### # of results returned by API call: ",
                len(df.index),
            )

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.caption("")
                check_box = st.checkbox(
                    "Ag-Grid mode", help="Tick this box to see your data in Ag-grid!"
                )
                st.caption("")

            with col2:
                st.caption("")
                st.checkbox(
                    "Widen layout",
                    key="widen",
                    help="Tick this box to switch the layout to 'wide' mode",
                )
                st.caption("")

            if not check_box:

                @st.cache
                def convert_df(df):
                    return df.to_csv().encode("utf-8")

                csv = convert_df(df)

                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="large_df.csv",
                    mime="text/csv",
                )

                st.caption("")

                st.dataframe(df, height=500)

            elif check_box:

                df = df.reset_index()

                gb = GridOptionsBuilder.from_dataframe(df)
                # enables pivoting on all columns, however i'd need to change ag grid to allow export of pivoted/grouped data, however it select/filters groups
                gb.configure_default_column(
                    enablePivot=True, enableValue=True, enableRowGroup=True
                )
                gb.configure_selection(selection_mode="multiple", use_checkbox=True)
                gb.configure_side_bar()
                gridOptions = gb.build()
                st.info(
                    f"""
                            💡 Tip! Hold the '⇧ Shift' key when selecting rows to select multiple rows at once!
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

    except ValueError as ve:

        st.warning("⚠️ You need to sign in to your Google account first!")

    except IndexError:
        st.info(
            "⛔ It seems you haven’t correctly configured Google Search Console! Click [here](https://support.google.com/webmasters/answer/9008080?hl=en) for more information on how to get started!"
        )

with tab2:

    st.write("")
    st.write("")

    st.write(
        """

    #### About this app

    * ✔️ One-click connect to the [Google Search Console API](https://developers.google.com/webmaster-tools)
    * ✔️ Easily traverse your account hierarchy
    * ✔️ Go beyond the [1K row UI limit](https://www.gsqi.com/marketing-blog/how-to-bulk-export-search-features-from-gsc/)
    * ✔️ Enrich your data querying with multiple dimensions layers and extra filters!

    ✍️ You can read the blog post [here](https://blog.streamlit.io/p/e89fd54e-e6cd-4e00-8a59-39e87536b260/) for more information.

    #### Going beyond the `25K` row limit

    * There's a `25K` row limit per API call on the [Cloud](https://streamlit.io/cloud) version to prevent crashes.
    * You can remove that limit by forking this code and adjusting the `RowCap` variable in the `streamlit_app.py` file

    #### Kudos

    This app relies on Josh Carty's excellent [Search Console Python wrapper](https://github.com/joshcarty/google-searchconsole). Big kudos to him for creating it!

    #### Questions, comments, or report a 🐛?

    * If you have any questions or comments, please DM [me](https://twitter.com/DataChaz). Alternatively, you can ask the [Streamlit community](https://discuss.streamlit.io).
    * If you find a bug, please raise an issue in [Github](https://github.com/CharlyWargnier/google-search-console-connector/pulls).

    #### Known bugs
    * You can filter any dimension in the table even if the dimension hasn't been pre-selected. I'm working on a fix for this.
    
    """
    )
