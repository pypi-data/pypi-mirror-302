"""
使用该cookies，可以获取页面的`_SSR_HYDRATED_DATA`

参考：https://github.com/soimort/you-get/blob/29f513821df4b0ec3ed0b514a0897f8c336b51e7/src/you_get/extractors/ixigua.py
"""

cookies = {
    'MONITOR_WEB_ID': '7892c49b-296e-4499-8704-e47c1b15123',
    '__ac_nonce': '060d88ff000a75e8d17eb',
    '__ac_signature': '_02B4Z6wo100f01kX9ZpgAAIDAKIBBQUIPYT5F2WIAAPG2ad',
    'ixigua-a-s': '1',
    'ttcid': 'af99669b6304453480454f1507011d5c234',
    'BD_REF': '1',
    'ttwid': '1%7CcIsVF_3vqSIk4XErhPB0H2VaTxT0tdsTMRbMjrJOPN8%7C1624806049%7C08ce7dd6f7d20506a41ba0a331ef96a6505d96731e6ad9f6c8c709f53f227ab1'
}

# cookies_string = '''
# fpk1=U2FsdGVkX1+sZMZHoYNkqR95mnHppjcyJnYHOj24krVXhUY5+Bgzxo1PtS0UeCoe7KYsshU5Knxrx/GNgXLQZA==; fpk2=362d7fe3d8b2581bffa359f0eeda7106; MONITOR_WEB_ID=eedf1dcf-e4cd-4073-b93c-a8470b7eff4a; s_v_web_id=verify_m017d4vv_nV5jZBzc_dbUN_46zV_84jo_Xtg3THIjy7bR; passport_csrf_token=7715e5d7ac6d6756fe8f16596b0dac8b; passport_csrf_token_default=7715e5d7ac6d6756fe8f16596b0dac8b; odin_tt=1ff6c0d60ec5fb74808be925fbdd2bf01f27750fda1b4351f1c8b75871141db2b3cd9e8115b5f0436c816d6ed67cb670; sid_guard=5b3f1de9be099782a730840e35ee4954%7C1724084474%7C5184001%7CFri%2C+18-Oct-2024+16%3A21%3A15+GMT; uid_tt=dbb79264aadb68929b686696f794e41e; uid_tt_ss=dbb79264aadb68929b686696f794e41e; sid_tt=5b3f1de9be099782a730840e35ee4954; sessionid=5b3f1de9be099782a730840e35ee4954; sessionid_ss=5b3f1de9be099782a730840e35ee4954; is_staff_user=false; sid_ucp_v1=1.0.0-KDQzZDI3NzZmMGJmNWYxODgzYTIxYTVkMDlmYjdjNDNiYzkxMDI5MjMKFwjVtJOX2QIQ-uGNtgYY6A0gDDgGQPQHGgJobCIgNWIzZjFkZTliZTA5OTc4MmE3MzA4NDBlMzVlZTQ5NTQ; ssid_ucp_v1=1.0.0-KDQzZDI3NzZmMGJmNWYxODgzYTIxYTVkMDlmYjdjNDNiYzkxMDI5MjMKFwjVtJOX2QIQ-uGNtgYY6A0gDDgGQPQHGgJobCIgNWIzZjFkZTliZTA5OTc4MmE3MzA4NDBlMzVlZTQ5NTQ; UIFID=945415714cc042aa2f3472e17f660569f2375ed0b3c2bc07fe097d8f64c152aad492e61cef09e6b76bc3c6864c6d71633e91990a0591b2130e8e8a03934d891b2ed8fb06528271abc48633aa524e287cf3168f5d9aed007705e2193a3ec2de0c21702d13fb99d47da6a97702a5bc2ce9415113c7d1c774bd4760cff67888f35d; first_enter_player=%7B%22any_video%22%3A%222.14.3%22%7D; gfkadpd=1768,30523; _tea_utm_cache_2285=undefined; __ac_nonce=067067eed003a769496b1; __ac_signature=_02B4Z6wo00f01v1As1wAAIDDITks6QMQXHL9YLfAANhj82; support_webp=true; support_avif=true; csrf_session_id=2d7f13b207f2179033ed7ff52ccd5267; ixigua-a-s=3; ttwid=1%7CmlaSoRhLsl8X24WDj5VyFwTJ3pK7Sy1Nrp8Q9t6MThc%7C1728479156%7Cc3d30e7741f37a7e2211fc6c480920c9605569541e2ab204656056d8dbb91066
# '''

# cookies = dict((item.strip().split('=', 1) for item in cookies_string.strip().split(';')))
# print(cookies)