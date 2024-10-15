# Copyright 2014 Facebook, Inc.

# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.

# As with any software that integrates with the Facebook platform, your use
# of this software is subject to the Facebook Developer Principles and
# Policies [http://developers.facebook.com/policy/]. This copyright notice
# shall be included in all copies or substantial portions of the software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# This file stores the information needed to perform integration testing
# on the Python Ads SDK.

class FieldName:
    ACCOUNT_ID = 'account_id'
    ACCOUNT_STATUS = 'account_status'
    ACTION_ATTRIBUTION_WINDOWS = 'action_attribution_windows'
    ACTION_BREAKDOWNS = 'action_breakdowns'
    ACTION_REPORT_TIME = 'action_report_time'
    ACTOR_ID = 'actor_id'
    AD_ACCOUNT_CREATED_FROM_BM_FLAG = 'ad_account_created_from_bm_flag'
    AD_FORMAT = 'ad_format'
    AD_ID = 'ad_id'
    AD_NAME = 'ad_name'
    AD_REVIEW_FEEDBACK = 'ad_review_feedback'
    ADLABELS = 'adlabels'
    ADSET_ID = 'adset_id'
    ADSET_SCHEDULE = 'adset_schedule'
    AGE = 'age'
    AGENCY_CLIENT_DECLARATION = 'agency_client_declaration'
    AMOUNT_SPENT = 'amount_spent'
    APPLINK_TREATMENT = 'applink_treatment'
    AUTHORIZATION_CATEGORY = 'authorization_category'
    AUTO_UPDATE = 'auto_update'
    ASSET_FEED_ID = 'asset_feed_id'
    BALANCE = 'balance'
    BID_ADJUSTMENTS = 'bid_adjustments'
    BID_AMOUNT = 'bid_amount'
    BID_STRATEGY = 'bid_strategy'
    BILLING_EVENT = 'billing_event'
    BODY = 'body'
    BOOSTED_OBJECT_ID = 'boosted_object_id'
    BRAND_LIFT_STUDIES = 'brand_lift_studies'
    BUDGET_REBALANCE_FLAG = 'budget_rebalance_flag'
    BUDGET_REMAINING = 'budget_remaining'
    BUSINESS_CITY = 'business_city'
    BUSINESS = 'business'
    BUYING_TYPE = 'buying_type'
    CALL_TO_ACTION_TYPE = 'call_to_action_type'
    CAMPAIGN_ID = 'campaign_id'
    CAN_CREATE_BRAND_LIFT_STUDY = 'can_create_brand_lift_study'
    CAN_USE_SPEND_CAP = 'can_use_spend_cap'
    CAPABILITIES = 'capabilities'
    CATEGORIZATION_CRITERIA = 'categorization_criteria'
    CONFIGURED_STATUS = 'configured_status'
    CREATED_TIME = 'created_time'
    CREATIVE = 'creative'
    CURRENCY = 'currency'
    DAILY_BUDGET = 'daily_budget'
    DAILY_MIN_SPEND_TARGET = 'daily_min_spend_target'
    DATE_PRESET = 'date_preset'
    DATE_FORMAT = 'date_format'
    DATE_START = 'date_start'
    DATE_STOP = 'date_stop'
    DISABLE_REASON = 'disable_reason'
    DYNAMIC_ASSET_LABEL = 'dynamic_asset_label'
    DYNAMIC_CREATIVE_SPEC = 'dynamic_creative_spec'
    EFFECTIVE_STATUS = 'effective_status'
    EXECUTION_OPTIONS = 'execution_options'
    EXTENDED_CREDIT_INVOICE_GROUP = 'extended_credit_invoice_group'
    FAILED_DELIVERY_CHECKS = 'failed_delivery_checks'
    HAS_PAGE_AUTHORIZED_ADACCOUNT = 'has_page_authorized_adaccount'
    HEIGHT = 'height'
    ID = 'id'
    IMAGE_HASH = 'image_hash'
    INCLUDE_DRAFTS = 'include_drafts'
    INSTAGRAM_ACTOR_ID = 'instagram_actor_id'
    INVOICE = 'invoice'
    ISSUES_INFO = 'issues_info'
    ITERATIVE_SPLIT_TEST_CONFIGS = 'iterative_split_test_configs'
    LAST_BUDGET_TOGGLING_TIME = 'last_budget_toggling_time'
    LEVEL = 'level'
    LIFETIME_BUDGET = 'lifetime_budget'
    NAME = 'name'
    OBJECTIVE = 'objective'
    OBJECT_URL = 'object_url'
    OPTIMIZATION_GOAL = 'optimization_goal'
    RECOMMENDATIONS = 'recommendations'
    RENDER_TYPE = 'render_type'
    REVIEW_FEEDBACK = 'review_feedback'
    PACING_TYPE = 'pacing_type'
    PRIORITY = 'priority'
    PROMOTED_OBJECT = 'promoted_object'
    SOURCE_CAMPAIGN_ID = 'source_campaign_id'
    SPECIAL_AD_CATEGORY = 'special_ad_category'
    SPEND_CAP = 'spend_cap'
    STATUS = 'status'
    SUMMARY_ACTION_BREAKDOWNS = 'summary_action_breakdowns'
    TARGETING = 'targeting'
    TIME_RANGE = 'time_range'
    TIMEZONE_ID = 'timezone_id'
    TITLE = 'title'
    TOPLINE_ID = 'topline_id'
    TOS_ACCEPTED = 'tos_accepted'
    TUNE_FOR_CATEGORY = 'tune_for_category'
    START_TIME = 'start_time'
    STOP_TIME = 'stop_time'
    UPDATED_SINCE = 'updated_since'
    UPDATED_TIME = 'updated_time'
    UPSTREAM_EVENTS = 'upstream_events'
    WIDTH = 'width'

class TestValue:
    ACCESS_TOKEN = 'accesstoken'
    ACCOUNT_ID = 'act_123'
    ACCOUNT_STATUS = 1
    ACTION_ATTRIBUTION_WINDOWS = '28d_click'
    ACTION_BREAKDOWNS = 'action_canvas_component_name'
    ACTION_REPORT_TIME = 'conversion'
    ACTOR_ID = '1245'
    AD_ACCOUNT_CREATED_FROM_BM_FLAG = 'false'
    AD_ID = '125475'
    AD_LABEL = '{"name": "test_label"}'
    AD_FORMAT = 'DESKTOP_FEED_STANDARD'
    AD_REVIEW_FEEDBACK = '{"global": "LANDING_PAGE_FAIL"}'
    ADSET_ID = '12345'
    ADSET_SCHEDULE = '{"pacing_type": "standard"}'
    AGE = '365'
    AGENCY_CLIENT_DECLARATION = (
        '{'
        '"agency_representing_client": "0",'
        '"client_based_in_france":"0",'
        '"client_city": "San Jose",'
        '"client_postal_code": "95131",'
        '"client_street": "lundi street"'
        '}'
    )
    AMOUNT_SPENT = "50000"
    APPLINK_TREATMENT = 'deeplink_with_web_fallback'
    APP_ID = '1234567'
    APP_SECRET = 'appsecret'
    APP_URL = 'http://test.com'
    ASSET_FEED_ID = '123'
    AUTHORIZATION_CATEGORY = 'NONE'
    AUTO_UPDATE = 'true'
    BALANCE = '25000'
    BID_ADJUSTMENTS = '{"user_groups": "test_group"}'
    BID_AMOUNT = '30000'
    BID_STRATEGY = 'LOWEST_COST_WITHOUT_CAP'
    BILLING_EVENT = 'IMPRESSIONS'
    BODY = "This is my test body"
    BOOSTED_OBJECT_ID = '12345678'
    BRAND_LIFT_STUDIES = (
        '{'
        '"id": "cell_id",'
        '"name":"Group A",'
        '"treatment_percentage": "50",'
        '"adsets": {"id" : "adset_id"}'
        '}'
    )
    BUDGET_REBALANCE_FLAG = 'false'
    BUDGET_REMAINING = '150'
    BUSINESS_CITY = 'Menlo park'
    BUSINESS_ID = '111111'
    BUSINESS = (
        '{'
        '"id": "111111",'
        '"name":"test business"'
        '}'
    )
    BUYING_TYPE = 'AUCTION'
    CALL_TO_ACTION_TYPE = 'CONTACT'
    CAMPAIGN_ID = '1234321'
    CAN_CREATE_BRAND_LIFT_STUDY = 'true'
    CAN_USE_SPEND_CAP = 'true'
    CAPABILITIES = 'BULK_ACCOUNT'
    CATEGORIZATION_CRITERIA = 'brand'
    CONFIGURED_STATUS = 'PAUSED'
    CREATED_TIME = '3728193'
    CREATIVE_ID = '1523548'
    CREATIVE = (
        '{'
        '"id": "15742462",'
        '"name": "test name"'
        '}'
    )
    CURRENCY = 'USD'
    DAILY_BUDGET = '200'
    DAILY_MIN_SPEND_TARGET = '50'
    DATE_FORMAT = 'U'
    DATE_PRESET = 'last_30d'
    DATE_START = '2019-11-06'
    DATE_STOP = '2019-12-05'
    DISABLE_REASON = 0
    DYNAMIC_ASSET_LABEL = 'test dynamic asset label'
    DYNAMIC_CREATIVE_SPEC = (
        '{'
        '"message": "test message",'
        '"description": "test description"'
        '}'
    )
    EFFECTIVE_STATUS = 'PAUSED'
    EXECUTION_OPTIONS = 'include_recommendations'
    EXTENDED_CREDIT_INVOICE_GROUP = (
        '{'
        '"id": "12325487",'
        '"name": "test name"'
        '}'
    )
    FAILED_DELIVERY_CHECKS = (
        '{'
        '"summary": "Custom Audience No Longer Shared",'
        '"description": "This custom audience not shared.",'
        '"check_name": "invalid_custom_audiences"'
        '}'
    )
    HAS_PAGE_AUTHORIZED_ADACCOUNT = 'true'
    HEIGHT = 690
    IMAGE_HASH = '9fdba2b8a67f316e107d3cbbfad2952'
    INCLUDE_DRAFTS = 'false'
    INSTAGRAM_ACTOR_ID = '12321'
    INVOICE = 'true'
    ISSUES_INFO = (
        '{'
        '"level": "AD",'
        '"error_code": "1815869",'
        '"error_summary": "Ad post is not available"'
        '}'
    )
    ITERATIVE_SPLIT_TEST_CONFIGS = '{"name": "test_config"}'
    LAST_BUDGET_TOGGLING_TIME = '3892193'
    LEVEL = 'ad'
    LIFETIME_BUDGET = '10000'
    NAME = 'test_name'
    OBJECTIVE = 'LINK_CLICKS'
    OBJECT_URL = 'http://test.object.com'
    OPTIMIZATION_GOAL = 'LINK_CLICKS'
    PACING_TYPE = 'standard'
    PAGE_ID = '13531'
    PRIORITY = '2'
    PROMOTED_OBJECT = '{"page_id": "13531"}'
    RECOMMENDATIONS = '{"code": "1772120"}'
    RENDER_TYPE = 'FALLBACK'
    REVIEW_FEEDBACK = 'test review'
    SECONDARY_BUSINESS_ID = '2222222'
    SECONDARY_ACCOUNT_ID = 'act_456'
    SECONDARY_PAGE_ID = '24642'
    SPECIAL_AD_CATEGORY = 'EMPLOYMENT'
    SPEND_CAP = '922337203685478'
    START_TIME = '3728232'
    STATUS = 'PAUSED'
    STOP_TIME = '3872293'
    SUMMARY_ACTION_BREAKDOWNS = 'action_device'
    TARGETING = (
        '{'
        '"geo_locations": {"countries": "US"},'
        '"interests":{"id": "12345678910", "name": "Parenting"}'
        '}'
    )
    TIME_RANGE =(
        '{'
        '"since": "2018-11-01",'
        '"until": "2019-11-01"'
        '}'
    )
    TIMEZONE_ID = '10'
    TITLE = 'test_title'
    TOPLINE_ID = '32123'
    TOS_ACCEPTED = (
        '{'
        '"item1": "1"'
        '}'
    )
    TUNE_FOR_CATEGORY = 'CREDIT'
    UPDATED_SINCE = '35487985'
    UPDATED_TIME = '3728132'
    UPSTREAM_EVENTS = '{"name": "event_1", "event_id": "12121"}'
    WIDTH = 540
