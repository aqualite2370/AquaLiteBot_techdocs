from __future__ import annotations

import json
import re
from pathlib import Path


BACKUP_PATH = Path("backend/data/documents.pre_rewrite_backup.json")
TARGET_PATH = Path("backend/data/documents.json")


MANUAL_REFINES: dict[str, dict[str, list]] = {
    "瀹氭椂绂佽█缇ゅ憳": {
        "desc": [
            "鐢ㄤ簬鍦ㄧ兢鍐呭垱寤恒€佹煡鐪嬪拰鍙栨秷瀹氭椂绂佽█浠诲姟銆?,
        ],
        "commands": [
            ("鍒涘缓瀹氭椂绂佽█浠诲姟銆?, "/mute 灏忔椂:鍒嗛挓 鍒嗛挓 QQ鍙?),
            ("鍙栨秷鎸囧畾鎴愬憳鐨勭瑷€浠诲姟銆?, "/unmute QQ鍙?),
            ("鏌ョ湅褰撳墠绂佽█浠诲姟鍒楄〃銆?, "/list_mute"),
        ],
        "notes": [
            "浠呯兢涓诲拰绠＄悊鍛樺彲鍒涘缓鎴栧垹闄ょ瑷€浠诲姟銆?,
        ],
    },
    "JmComic婕敾涓嬭浇": {
        "desc": [
            "鐢ㄤ簬鎸?ID 涓嬭浇 JmComic 璧勬簮骞惰繑鍥炵粨鏋溿€?,
            "妯″潡宸插姞鍏ュ紑鍏抽€夐」锛屼究浜庢寜闇€鍚仠銆?,
        ],
        "commands": [
            ("鎸?ID 涓嬭浇婕敾璧勬簮銆?, "jm[id]"),
        ],
        "links": [
            "https://github.com/hect0x7/JMComic-Crawler-Python",
        ],
    },
    "鐩稿叧淇℃伅": {
        "desc": [
            "寮€鍙戣€呰仈绯绘柟寮忥細濂惰尪sama锛圦Q锛?259891410锛夈€?,
            "缇よ亰涓浆绔欙細775402634銆?,
            "鍘?2/3/4 缇ゅ凡瑙ｆ暎锛岃浠ヤ腑杞兢鍏憡涓哄噯銆?,
        ],
    },
    "B绔欒棰戣В鏋?: {
        "desc": [
            "鐢ㄤ簬瑙ｆ瀽 B 绔欏垎浜摼鎺ュ苟鍦?QQ 涓洿鎺ユ挱鏀俱€?,
            "璇峰厛鍦?B 绔欒棰戦〉鐐瑰嚮鈥滃垎浜€濓紝鍐嶅鍒堕摼鎺ヤ綔涓哄弬鏁般€?,
        ],
        "commands": [
            ("瑙ｆ瀽 B 绔欏垎浜摼鎺ャ€?, "bili [鍒嗕韩閾炬帴]"),
            ("浣跨敤鍚屼箟鍓嶇紑瑙﹀彂瑙ｆ瀽銆?, "bili / b绔欒В鏋?/ B绔欒В鏋?[鍒嗕韩閾炬帴]"),
        ],
    },
    "琛ㄦ儏鍖呭埗浣?: {
        "desc": [
            "鏀寔鎸夊叧閿瘝蹇€熺敓鎴愭垨璋冪敤琛ㄦ儏鍖呮ā鏉裤€?,
            "鍙煡鐪嬭〃鎯呭弬鏁拌鏄庝笌棰勮鍥俱€?,
        ],
        "commands": [
            ("鎸夋ā鏉胯鍒欑敓鎴愯〃鎯呫€?, "鍏抽敭璇?+ 鍥剧墖/鏂囧瓧/@鏌愪汉"),
            ("鏌ョ湅鍏抽敭璇嶅搴旂殑琛ㄦ儏鍙傛暟涓庨瑙堛€?, "琛ㄦ儏璇︽儏 + 鍏抽敭璇?),
            ("蹇€熸墦寮€鍔熻兘璇存槑鍏ュ彛銆?, "琛ㄦ儏鍖呭埗浣?),
        ],
    },
    "娲诲瓧鍗板埛": {
        "desc": [
            "鐢ㄤ簬鐢熸垚娲诲瓧鍗板埛椋庢牸鐨勬枃鏈晥鏋溿€?,
        ],
        "commands": [
            ("鏌ョ湅璇ュ姛鑳界殑鍙傛暟涓庡府鍔┿€?, "hzys -h"),
        ],
    },
    "鐢ㄥ墠蹇呰锛侊紒": {
        "desc": [
            "鎷夌兢鍓嶈鍏堝姞鍏ヤ腑杞兢锛?75402634锛屽苟鏍规嵁缇ゅ叕鍛婃彁渚涚洰鏍囩兢淇℃伅銆?,
            "濡傛湁闂鎴栧弽棣堬紝鍙仈绯诲ザ鑼秙ama锛圦Q锛?259891410锛夈€?,
        ],
        "notes": [
            "璇蜂弗鏍兼敞鎰忓懡浠や腑鐨勭┖鏍间笌鍙傛暟鏍煎紡锛孾] 鍐呴€氬父琛ㄧず鈥滈渶瑕佹浛鎹负瀹為檯鍙傛暟鈥濄€?,
            "鍛戒护闀挎椂闂存棤鍝嶅簲鏃讹紝璇峰厛鏍稿绀轰緥鍥捐緭鍏ユ牸寮忥紝鍐嶅彂閫佲€滀綘濂解€濇鏌?Bot 鍦ㄧ嚎鐘舵€併€?,
        ],
    },
    "MaimaiDX锛堣垶钀岋級妯″潡": {
        "desc": [
            "鏀寔鏌ヨ MaimaiDX 涓汉鏈€浣虫垚缁╋紙Best40 / Best50锛夈€?,
        ],
        "commands": [
            ("鏌ヨ涓汉 Best40銆?, "/mai b40"),
            ("鏌ヨ涓汉 Best50銆?, "/mai b50"),
        ],
        "notes": [
            "棣栨浣跨敤鍓嶉渶鍏堝湪澶栭儴绔欑偣瀹屾垚璐﹀彿缁戝畾锛屽苟鍦ㄤ釜浜轰俊鎭腑缁戝畾 QQ銆?,
        ],
        "links": [
            "https://www.diving-fish.com/maimaidx/prober/",
        ],
    },
    "馃尒": {
        "desc": [
            "濞变箰浜掑姩鍔熻兘锛屽彲棰嗗彇闅忔満灏忕ぜ鍖呫€?,
        ],
        "commands": [
            ("瑙﹀彂闂數浜掑姩浜嬩欢銆?, "鍔堟垜"),
        ],
        "notes": [
            "褰?Bot 鍏锋湁绠＄悊鏉冮檺涓旂洰鏍囦负缇ゅ憳鏃讹紝鍙兘闅忔満瑙﹀彂 1-300 绉掔瑷€銆?,
        ],
    },
    "鑸炶悓灏忛粦灞?: {
        "desc": [
            "鑸炶悓鐩稿叧濞变箰鍔熻兘锛屽叿浣撴晥鏋滆鍙傝€冪ず渚嬪浘銆?,
        ],
    },
    "Valorant妯″潡": {
        "desc": [
            "璇ユā鍧椾緷璧栧缃戠幆澧冿紝鍥藉唴缃戠粶鐜涓嬪彲鑳芥棤娉曠ǔ瀹氫娇鐢ㄣ€?,
            "鏀寔缁戝畾璐﹀彿骞舵煡璇㈠晢搴楄疆鎹俊鎭€?,
        ],
        "commands": [
            ("缁戝畾璐﹀彿锛堝缓璁鑱婁娇鐢級銆?, "/valbind[璐︽埛鍚峕#[瀵嗙爜]"),
            ("鏌ヨ褰撳墠鍟嗗簵杞崲銆?, "/val shop"),
            ("涓枃鍒悕瑙﹀彂鍟嗗簵鏌ヨ銆?, "鐡﹀晢搴?),
        ],
        "notes": [
            "鑻ヨ处鍙峰紑鍚簩娆￠獙璇侊紝鍙兘瀵艰嚧缁戝畾澶辫触銆?,
            "璇峰嬁鍦ㄥ叕寮€缇よ亰涓彂閫佹晱鎰熻处鍙蜂俊鎭€?,
        ],
    },
    "鍦ㄧ嚎杩愯浠ｇ爜": {
        "desc": [
            "鐢ㄤ簬鍦ㄧ嚎璋冭瘯灏忓瀷绠楁硶鎴栦唬鐮佺墖娈碉紝杩斿洖鏍囧噯杈撳嚭缁撴灉銆?,
        ],
        "commands": [
            ("鎸夎瑷€鎵ц浠ｇ爜鍧椼€?, "code c/cpp/c#/py/php/go/java/js"),
        ],
        "notes": [
            "棣栬鎸囧畾璇█锛屽悗缁唴瀹逛负浠ｇ爜涓讳綋銆?,
        ],
    },
    "濂惰尪鎶藉": {
        "desc": [
            "缇ゅ唴浜掑姩鎶藉鍔熻兘锛屽彲鎸夋鏁拌繛缁弬涓庛€?,
        ],
        "commands": [
            ("鍙備笌涓€娆℃娊濂栥€?, "鎶藉ザ鑼?),
            ("鎸夋寚瀹氭鏁拌繛缁娊濂栥€?, "鎶藉ザ鑼禰娆℃暟]"),
        ],
        "notes": [
            "鍙戣捣鎶藉鍓嶈嚦灏戦渶瑕佷袱鏉ザ鑼躲€?,
        ],
    },
    "OSU锛佹ā鍧?: {
        "desc": [
            "鏀寔 OSU 璋遍潰鎼滅储涓庝笅杞芥帹閫併€?,
        ],
        "commands": [
            ("鎸夊叧閿瘝鎼滅储璋遍潰銆?, "/osu mapsec[鍏抽敭璇峕"),
            ("鎸?SID 涓嬭浇骞舵帹閫佽氨闈㈡枃浠躲€?, "/osudl [sid]"),
        ],
    },
    "Furry鎼?闅忔満鍥?: {
        "desc": [
            "鍩轰簬 e621 鐨勬悳绱笌闅忔満鍥惧姛鑳斤紝鏀寔澶氭爣绛剧粍鍚堟绱€?,
        ],
        "commands": [
            ("鎸夊叧閿瘝鎼滅储銆?, "/e621 sec[鎼滅储璇峕"),
            ("鎸?ID 鑾峰彇鎸囧畾鍥剧墖銆?, "/e621 get[鍥剧墖id]"),
            ("鎸夊叧閿瘝闅忔満杩斿洖鍥剧墖銆?, "/e621 rand[鎼滅储璇峕"),
            ("绠€鍐欓殢鏈烘悳绱€?, "er[鍏抽敭璇峕"),
            ("鍏ㄩ殢鏈烘ā寮忋€?, "er"),
        ],
        "notes": [
            "澶氭爣绛惧彲浣跨敤 # 鍒嗛殧锛屼緥濡傦細dragon#strong銆?,
            "浣跨敤 @ 鍏ㄥ睍绀烘ā寮忔椂杩斿洖鏉℃暟浼氬噺灏戙€?,
        ],
    },
    "濂惰尪閰遍櫔鑱?: {
        "desc": [
            "鍩轰簬灏忕埍 API 鐨勮亰澶╂ā鍧楋紝鍙繘琛屾棩甯稿璇濄€?,
        ],
        "commands": [
            ("鑹剧壒 Bot 骞跺彂閫佽鍙ヨ繘琛屽璇濄€?, "@Bot + 璇彞"),
        ],
    },
    "娓告垙寮€榛戞憞浜烘ā鍧?: {
        "desc": [
            "鐢ㄤ簬绠＄悊寮€榛戞父鎴忓垪琛ㄥ拰鍙戣捣鎽囦汉鎻愰啋銆?,
        ],
        "commands": [
            ("鏌ョ湅褰撳墠寮€榛戞父鎴忓垪琛ㄣ€?, "娓告垙鍒楄〃"),
            ("鍙戣捣鏌愭娓告垙鐨勬憞浜恒€?, "鐜╀笉鐜娓告垙鍚峕 / 鎵撲笉鎵揫娓告垙鍚峕"),
            ("鍔犲叆寮€榛戝垪琛ㄣ€?, "鍔犲叆娓告垙鍒楄〃[娓告垙鍚峕"),
            ("閫€鍑哄紑榛戝垪琛ㄣ€?, "閫€鍑烘父鎴忓垪琛╗娓告垙鍚峕"),
        ],
    },
    "涓栫晫璁″垝pjsk琛ㄦ儏鍖呭埗浣?: {
        "desc": [
            "鐢ㄤ簬鐢熸垚涓栫晫璁″垝锛圥JSK锛夐鏍兼枃鏈〃鎯呭浘銆?,
        ],
        "commands": [
            ("鎸夋枃鏈唴瀹圭敓鎴愬浘鐗囥€?, "pjsk[鏂囨湰鍐呭]"),
        ],
        "notes": [
            "鏂囨湰涓殑绌烘牸浼氳澶勭悊涓烘崲琛屻€?,
        ],
    },
    "ACC璁＄畻鍣?: {
        "desc": [
            "鐢ㄤ簬璁＄畻娓哥帺鎴愮哗鐩稿叧 ACC 鏁版嵁銆?,
        ],
        "commands": [
            ("杩涘叆 ACC 璁＄畻娴佺▼銆?, "/acc"),
        ],
        "notes": [
            "鎸夋彁绀烘楠や緷娆¤緭鍏ュ弬鏁板嵆鍙€?,
        ],
    },
    "濂惰尪鎺掕姒?: {
        "desc": [
            "鏌ョ湅缇ゅ唴濂惰尪鏁伴噺鎺掕銆?,
        ],
        "commands": [
            ("鑾峰彇濂惰尪鎺掕姒溿€?, "濂惰尪鎺掕"),
        ],
    },
    "鎴充竴鎴?鎷嶄竴鎷?: {
        "desc": [
            "濞变箰浜掑姩鍔熻兘锛岀洿鎺ユ埑濂惰尪閰卞嵆鍙Е鍙戙€?,
        ],
    },
    "鍥剧墖閴磋祻鍒嗘瀽锛?: {
        "desc": [
            "鐢ㄤ簬瀵瑰浘鐗囪繘琛岄壌璧忔垨鍒嗘瀽杈撳嚭銆?,
        ],
        "commands": [
            ("鍒嗘瀽鍥剧墖鍐呭銆?, "/鍒嗘瀽 + 鍥剧墖"),
            ("閴磋祻鍥剧墖椋庢牸銆?, "/閴磋祻 + 鍥剧墖"),
        ],
    },
    "Arcaea妯″潡锛堝凡涓嶅彲鐢級": {
        "desc": [
            "璇ユā鍧楀綋鍓嶅凡鍋滆繍锛屾殏涓嶅彲浣跨敤銆?,
        ],
        "notes": [
            "涓婃父鏈嶅姟涓嶅彲鐢ㄥ鑷村姛鑳戒笅绾裤€?,
        ],
    },
    "宸ヤ綔鎬т环姣旇绠楀櫒": {
        "desc": [
            "鐢ㄤ簬璇勪及宸ヤ綔鏀剁泭涓庢姇鍏ョ殑鎬т环姣斻€?,
        ],
        "commands": [
            ("鍚姩宸ヤ綔鎬т环姣旇绠楁祦绋嬨€?, "宸ヤ綔鎬т环姣?),
        ],
    },
    "鑸炵珛鏂规ā鍧?: {
        "desc": [
            "鎻愪緵鑸炵珛鏂硅处鍙风粦瀹氫笌鎴愮哗鏌ヨ鑳藉姏銆?,
        ],
        "commands": [
            ("缁戝畾璐﹀彿锛堝缓璁鑱婅繘琛岋級銆?, "/wlf bind"),
            ("瀹屾垚鎵爜鍚庤繘琛屼簩娆＄‘璁ゃ€?, "/wlf bindsec"),
            ("鏌ヨ璐﹀彿鍩虹淇℃伅銆?, "/wlf"),
            ("鎸夋洸鍚嶆悳绱€?, "/wlf sec[姝屾洸鍚峕"),
            ("鎸夎氨闈?ID 鎼滅储銆?, "/wlf secid[璋遍潰id]"),
            ("鏌ヨ鎸囧畾鎴愮哗銆?, "/wlf 鏌ュ垎[绫诲瀷][鏇插悕]"),
            ("妯＄硦鏌ヨ鎴愮哗銆?, "/wlf 妯＄硦鏌ュ垎[绫诲瀷][鏇插悕]"),
            ("鏌ョ湅鏈€浣虫垚缁╁墠 20銆?, "/wlf best"),
            ("鏌ョ湅鏈€鏂版洸鐩垚缁┿€?, "/wlf 鏂版洸鎴愮哗"),
        ],
        "notes": [
            "鎺ㄨ崘浣跨敤寰俊鎵爜锛屼笉寤鸿浣跨敤鑸炵珛鏂?App 鎵爜銆?,
            "/wlf best 鍙楁秷鎭簨浠堕檺鍒讹紝绉佽亰涓彲鑳芥棤娉曚娇鐢ㄣ€?,
        ],
    },
    "Phigros妯″潡": {
        "desc": [
            "鏀寔 Phigros 鏇茬洰淇℃伅鏌ヨ涓庢妧宸ф彁绀恒€?,
        ],
        "commands": [
            ("鎸夋洸鍚嶇簿纭煡璇€?, "/phi song[鏇茬洰鍚峕"),
            ("鎸夊叧閿瘝妯＄硦鎼滅储銆?, "/phi sec[鍏抽敭璇峕"),
            ("鏌ョ湅鐜╂硶鎻愮ず銆?, "/phi tip"),
        ],
        "notes": [
            "鏁版嵁鍐呭鏉ユ簮浜庤悓濞樼櫨绉戙€?,
        ],
    },
    "甯綘浣滈€夋嫨锛?: {
        "desc": [
            "鐢ㄤ簬鍦ㄥ涓€欓€夐」涓揩閫熼殢鏈哄喅绛栥€?,
        ],
        "commands": [
            ("鍦ㄥ涓€夐」涓殢鏈虹粰鍑虹粨鏋溿€?, "/甯垜閫夋嫨[閫夐」1]鎴朳閫夐」2]..."),
        ],
    },
    "浠婃棩浜哄搧锛?: {
        "desc": [
            "姣忔棩濞变箰鍔熻兘锛岃繑鍥炲綋鍓嶄汉鍝佸€笺€?,
        ],
        "commands": [
            ("鏌ヨ浠婃棩浜哄搧銆?, "浠婃棩浜哄搧"),
        ],
    },
    "鍥剧墖浜屾鍏冨寲锛?: {
        "desc": [
            "灏嗚緭鍏ュ浘鐗囪浆鎹负浜屾鍏冮鏍兼晥鏋溿€?,
        ],
        "commands": [
            ("鎻愪氦鍥剧墖杩涜浜屾鍏冨寲銆?, "/浜屾鍏冨寲 + 鍥剧墖"),
        ],
    },
    "绛惧埌锛?: {
        "desc": [
            "鎻愪緵姣忔棩绛惧埌鍜屽ザ鑼舵暟閲忔煡璇€?,
        ],
        "commands": [
            ("瀹屾垚姣忔棩绛惧埌銆?, "绛惧埌 /sign"),
            ("鏌ョ湅涓汉濂惰尪鎸佹湁鏁伴噺銆?, "!mm / 鎴戠殑濂惰尪"),
        ],
    },
    "Emoji鍚堟垚": {
        "desc": [
            "灏嗕袱涓?Emoji 鍚堟垚涓烘柊鐨勮〃鎯呯粨鏋溿€?,
        ],
        "commands": [
            ("杈撳叆涓や釜 Emoji 杩涜鍚堟垚銆?, "emoji + emoji"),
        ],
        "notes": [
            "鏆備笉鏀寔璇嗗埆 QQ 涓撴湁琛ㄦ儏銆?,
        ],
    },
    "鐐规瓕锛?: {
        "desc": [
            "鏀寔澶氬钩鍙板叧閿瘝鐐规瓕銆?,
        ],
        "commands": [
            ("QQ 闊充箰鐐规瓕銆?, "/qq鐐规瓕 [鍏抽敭璇峕"),
            ("缃戞槗浜戠偣姝屻€?, "/缃戞槗鐐规瓕 [鍏抽敭璇峕"),
            ("閰锋垜鐐规瓕銆?, "/閰锋垜鐐规瓕 [鍏抽敭璇峕"),
            ("閰风嫍鐐规瓕銆?, "/閰风嫍鐐规瓕 [鍏抽敭璇峕"),
            ("鍜挄鐐规瓕銆?, "/鍜挄鐐规瓕 [鍏抽敭璇峕"),
            ("B 绔欑偣姝屻€?, "/b绔欑偣姝?[鍏抽敭璇峕"),
        ],
        "notes": [
            "鍛戒护鍓嶇紑闇€鍖呭惈 / 銆?,
        ],
    },
    "EPIC姣忔棩鍏嶈垂娓告垙鎺ㄩ€?: {
        "desc": [
            "鐢ㄤ簬鏌ヨ EPIC 褰撳墠鍏嶈垂娓告垙淇℃伅銆?,
        ],
        "commands": [
            ("鑾峰彇姣忔棩鍏嶈垂娓告垙鎺ㄩ€併€?, "鍠滃姞涓€"),
        ],
    },
    "濂惰尪閰辩殑杩囧幓": {
        "desc": [
            "鍘嗗彶鏂囨。褰掓。椤碉紝璁板綍鏃х増鏈祫鏂欏叆鍙ｄ笌杩佺Щ璇存槑銆?,
        ],
        "links": [
            "https://www.showdoc.com.cn/ncj114514/8843059108042576",
            "https://note.youdao.com/ynoteshare1/index.html?id=31dc3ca4d79fdcc36240e95d4de06198&type=note",
        ],
    },
}


def extract_images(content: str) -> list[str]:
    return re.findall(r"!\[[^\]]*\]\([^)]+\)", content or "")


def extract_links(content: str) -> list[str]:
    urls = re.findall(r"https?://[^\s)]+", content or "")
    out = []
    for u in urls:
        if "note.youdao.com/yws/public/resource" in u:
            continue
        if u not in out:
            out.append(u)
    return out


def build_markdown(title: str, source_content: str, spec: dict[str, list]) -> str:
    desc = spec.get("desc", [])
    commands = spec.get("commands", [])
    notes = spec.get("notes", [])

    links = []
    for u in spec.get("links", []):
        if u not in links:
            links.append(u)
    for u in extract_links(source_content):
        if u not in links:
            links.append(u)

    images = extract_images(source_content)

    parts: list[str] = [f"# {title}", "", "## 鎻忚堪"]
    if desc:
        parts.extend([f"- {item}" for item in desc])
    else:
        parts.append("- 璇峰弬鑰冧笅鏂瑰姛鑳借鏄庝笌绀轰緥銆?)

    if commands:
        parts.extend(["", "## 浣跨敤"])
        for feature, command in commands:
            parts.append("```")
            parts.append(f"鍔熻兘璇存槑: {feature}")
            parts.append(f"瑙﹀彂鍛戒护: {command}")
            parts.append("```")
            parts.append("")
        if parts[-1] == "":
            parts.pop()

    if notes:
        parts.extend(["", "## 娉ㄦ剰"])
        parts.extend([f"- {item}" for item in notes])

    if links:
        parts.extend(["", "## 鍙傝€冮摼鎺?])
        parts.extend([f"- {u}" for u in links])

    if images:
        parts.extend(["", "## 绀轰緥", ""])
        for img in images:
            parts.append(img)
            parts.append("")
        if parts[-1] == "":
            parts.pop()

    return "\n".join(parts).strip() + "\n"


def main() -> None:
    source_payload = json.loads(BACKUP_PATH.read_text(encoding="utf-8"))
    target_payload = json.loads(TARGET_PATH.read_text(encoding="utf-8"))

    source_by_id = {d["id"]: d for d in source_payload.get("documents", [])}

    rewritten = 0
    for doc in target_payload.get("documents", []):
        source_doc = source_by_id.get(doc["id"], doc)
        title = source_doc.get("title", doc.get("title", "鏈懡鍚嶆枃妗?))
        spec = MANUAL_REFINES.get(title, {})
        new_content = build_markdown(title, source_doc.get("content", ""), spec)
        if doc.get("content") != new_content:
            doc["content"] = new_content
            rewritten += 1

    TARGET_PATH.write_text(json.dumps(target_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"manually_refined_docs={rewritten}")


if __name__ == "__main__":
    main()

