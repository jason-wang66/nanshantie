const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, 
        AlignmentType, PageBreak, HeadingLevel, BorderStyle, WidthType } = require('docx');
const fs = require('fs');

// 修订后的15款茶内容
const teaData = [
  {
    name: "童濛",
    fullName: "童濛 白毫银针 ·春·",
    story: "春山初醒，晨雾未散。露水从叶尖滑落，跌进泥土里，发出极轻的声响。有个孩子赤脚走过山径，衣襟上沾着青草的汁液，眼睛像刚洗过的天空。他看什么都新鲜，看什么都欢喜。山雀掠过，他仰头；野花绽放，他俯身。他叫童濛——是万物初生时的模样，是天地间第一缕干净的呼吸。",
    flavor: "头采头芽，白毫覆身如雪。沸水激扬之下，茶毫在杯中翻涌如雾，是早春尚未散尽的晨霜，是山间第一缕破云而出的光。入口，是意料之中的鲜——却比想象中更柔，像露珠滑过舌尖，来不及捕捉便已化开。汤至三巡，那一点若有似无的花香才慢悠悠浮上来，是它藏着的秘密，等你慢慢发现。",
    value: "不必急。三月采的银针，此刻正嫩。收下它，不必开封，偶尔想起便好。待到来年或更久，彼时的鲜会慢慢收敛，化作另一种温厚——那时再启封，你会知道，它没有辜负等待。",
    rank: "一盏春山，敬头拨的光。",
    quote: "「溪声便是广长舌，山色无非清净身」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-22.png?sign=1780650425-2f028f2aa4-0-ea9ec162d886e59da0033794b9fbdd3a78037ba95b1079419fc39c51afacd542",
    quoteImage: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-29.png?sign=1780650425-e32a5df045-0-aadd2d3b76d5cc4f8efc9acd4d811befca80192e380fa0e28ac54bc1730f33d0"
  },
  {
    name: "浮岚",
    fullName: "浮岚 福建高山绿茶 ·春·",
    story: "午后，山谷里起了雾。不是浓得化不开的那种，而是轻薄的，游走的，像是山在呼吸。雾从溪面升起，绕过松林，在半山腰停住。有个少年站在雾里，衣袂被风轻轻吹起，看不清面容，只觉得他整个人都像是从云中长出来的。他叫浮岚——是山与天的交界，是看得见却握不住的轻盈。",
    flavor: "1200米的云雾，造就了这杯茶的清骨架。茶汤入口，第一个感觉是\"轻\"——不是寡淡的轻，是山岚掠过山巅、不带走一片叶子的那种轻盈。鲜是底色，板栗香是山野的馈赠。一杯下去，喉间回甘如溪水漫过石涧，带着松风与露水的余韵。",
    value: "趁鲜。绿茶不等人，明前的鲜，过了明前便少一分。山路太远，快递太慢，唯有此刻的一口鲜爽，是往后多少年都追不回的。买回去，放进冰箱，偶尔打开闻一闻——那是你存下的一小片山林。",
    rank: "不必攀高岭，此间即云上。",
    quote: "「山色空蒙雨亦奇，水光潋滟晴方好」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-31.png?sign=1780650425-3371dcb154-0-341fb516825a7734170fa3f2b7fa89e777f5c1bd96dc29fc3caeb9b9de378eaf",
    quoteImage: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-38.png?sign=1780650425-6a2448a73c-0-26f3eb7e31ab829bafd96f74a5e9d60a829f78ba74449697acebf2c0bdfb4664"
  },
  {
    name: "不器",
    fullName: "不器 白牡丹 ·夏·",
    story: "夏日漫长，蝉声如织。树荫下坐着一个人，他面前摆着粗陶碗，碗里盛着清水。有人来问路，他指；有人来借火，他给；有人来闲谈，他听。他不拒绝任何人，也不强留任何人。他的性子温和，不偏不倚，像是山间的风，吹过就算了。他叫不器——君子不器，他什么都是，也什么都不是。",
    flavor: "白牡丹不以霸道理世，它走的是另一条路：一二级鲜叶，在水中缓缓舒展如花。一芽一二叶，恰到好处的成熟度，赋予了它白茶中最盛的花香。嗅之，是初夏茉莉将绽未绽时的清甜；饮之，是毫香托底、花香层层递进的温柔。尾水处，蜜甜收尾，不争不抢。",
    value: "它的香气会老去。三五年后，花香渐隐，蜜甜渐显，杯中便是另一种风景了。若你想留住此刻的芬芳——此刻便是最好的时刻；若你愿意等，它会还你一个更醇的自己。",
    rank: "不器，不拘一格，恰到好处。",
    quote: "「万物静观皆自得，四时佳兴与人同」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-40.png?sign=1780650425-b862b0b413-0-9606ce86a8c66e08949b688ad9106cad101963e5edee957485b213f21105daed",
    quoteImage: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-47.png?sign=1780650425-727c3d3efe-0-61c689552d9298b16bee591d65af8d409825e49106c3d91003de4492bf74a7ce"
  },
  {
    name: "丹桂",
    fullName: "丹桂 桂花红茶 ·秋·",
    story: "入秋之前，院子里那棵桂树先开了花。不是满树金黄，只是疏疏几簇，香气却已经藏不住了。有个女子在树下铺了竹匾，将落花拢在一起。她动作很轻，怕惊扰了那些细小的花瓣。她叫丹桂——不是秋天的全部，却是秋天最让人惦记的那一部分。",
    flavor: "不是春茶，却有秋日的圆满。窨制工艺让桂花与红茶相融，红是底色，桂是灵魂。茶汤入喉，桂香先行，甜蜜后至，像秋天第一个早晨推开窗——桂花香扑面而来，紧接着是炭火与熟果的暖意。不烈，不腻，是恰到好处的温柔。",
    value: "限定的不止是季节，也是风味。桂花香最盛时窨制，那一点秋意便封存在了茶里。入秋后启封，约三两好友，或是独自一人，以滚水唤醒那沉睡的桂花——这一口，是属于你的秋天。",
    rank: "一季桂香，值一个秋天。",
    quote: "「何当共剪西窗烛，却话巴山夜雨时」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-50.png?sign=1780650425-03eb945612-0-fcfdad2393a45bb4c252ad8eea7b7913e93c6b37c02761cb3af25ae376ba2937",
    quoteImage: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-57.png?sign=1780650425-5ec9cca8b3-0-e4478228599596011e7b9031dcbd454d248e0cac5404558067fa5b6b87be5693"
  },
  {
    name: "桂兰",
    fullName: "桂兰 肉桂 ·秋·",
    story: "秋天深了，山里的桂树与兰草同开。桂是浓的，香得热烈，隔着几道弯都能闻见；兰是淡的，清清冷冷，不走近便不知道。有个人，她身上既有桂的冲，又有兰的静。她走路带风，说话却轻；她性子烈，却从不伤人。山里人都说，她像一壶滚水冲下去的肉桂——初闻凌厉，再品回甘。她叫桂兰，是秋天最复杂的那一口。",
    flavor: "桂皮香是它递出的第一张名片，张扬、霸气、不容商量。入口，辛辣感如岩上劈下一道闪电，在舌面上划出微微的麻与热。但别急着下定论——三秒之后，花果的甜从岩韵深处浮起，与先前的霸道握手言和。这杯茶说的是：我不温柔，但我的温柔，你得等。",
    value: "肉桂不驯，急不得。新茶锐利，像刚出鞘的剑；三年五年后，那股锐气慢慢内化为沉稳，岩韵从张扬变为深沉。养它，是养一种等待的耐心；品它，是品时间如何打磨一泡茶的性格。",
    rank: "岩上百年，方得一味霸道。",
    quote: "「路遥知马力，日久见人心」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-60.png?sign=1780650425-b8fd199a75-0-483047066ba103ce2c68220c9b06e29ac20275bb58d27a1845d534a435a94428",
    quoteImage: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-67.png?sign=1780650425-9b2d6d43fb-0-2dd4303a70d6521b6364315d41c4098cf9c2c89d8ba528af2b4e13293a11dad2"
  },
  {
    name: "听枞",
    fullName: "听枞 老枞 ·秋·",
    story: "深山里有棵老枞，树龄已不可考。他常坐在树下，听风穿过枝叶的声音。风来时，树叶沙沙响，像是在说些什么。他听了几十年，从少年听到白头，终于听懂了——原来风什么也没说，是他自己心里有话。他养了条边牧，取名风声。风声风声，风过留声，人过留名。",
    flavor: "老枞不说自己的年纪，但茶汤会告诉你。百年光阴，从苔藓爬过的树干上流进茶汤，带着青苔的润、粽叶的清、还有一丝丝难以言说的幽。这杯茶需要慢品：第一口是粽叶香，第二口是木质甜，第三口……你仿佛能听到风穿过老枝的声音。它不是在喝茶，它是在听。",
    value: "养一泡老枞，是养一段不会重来的光阴。老枞树越来越少了，能存下来的老枞茶，每一泡都是限量版。它不急，你也别急。让它陪着你，慢慢老去——不是茶老了，是你与它一起老。",
    rank: "百年光阴，一盏枞韵。",
    quote: "「此时无声胜有声，别有幽愁暗恨生」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-70.png?sign=1780650425-13b2e74e4e-0-132cdf910b8510c20f7677e46faaafe8558d7254eba2ffafb03729b32476e76d",
    quoteImage: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-77.png?sign=1780650425-74a2cd83fe-0-e507d6830671627f224caa6acdaf14ced86f591d2ed7e65370a81c7f17bd151a"
  },
  {
    name: "天香",
    fullName: "天香 大红袍 ·秋·",
    story: "他不是茶人，但他爱茶。他不懂制茶，但他懂品茶。他住在山间一处僻静院落，院中植兰养桂，墙上挂着一幅「天香」的匾额。有人问天香是什么意思，他说天香就是天上的香气，不是人间能有的。有人再问，那你为什么喜欢，他说，因为人间太苦，需要一点天上的味道。他养了条罗威纳，取名王者。王者王者，王者风范，不怒自威。",
    flavor: "大红袍不说自己好。它只是安静地在那里，岩韵沉沉，像深山老刹里的暮鼓晨钟。茶汤入口，岩骨先行——那是岩石缝隙里长出来的茶才有的骨骼感，厚重而不沉重。继而是花香，不夺目，不张扬，是山岚经过兰草时顺手捎带的那一缕幽香。回甘悠长，是它最后说的话，说完便退场，不拖泥带水。",
    value: "若你存它，就不要急着喝。大红袍的岩韵需要时间唤醒，三年、五年、十年……每一年的打开都是不同的它。但若你只想认识它，此刻也不晚——它从不让人失望，只是有时让你等得更久。",
    rank: "岩骨花香，天香一脉。",
    quote: "「天生我材必有用，千金散尽还复来」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-80.png?sign=1780650425-4d845ec843-0-1bee14519328cca44dc2b2f5a6edca70355ed132d935a9b1ffa39fcc6e1d6250",
    quoteImage: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-87.png?sign=1780650425-77529b00b9-0-6d729ba0b479b39a3914c8d8429c47e37af48592ea7f3e3b1e1274126321c8e5"
  },
  {
    name: "履霜",
    fullName: "履霜 工夫红茶 ·冬·",
    story: "第一场霜落下来的时候，她来了。她穿着素色的衣裳，走路很轻，踩在霜叶上，发出细微的碎裂声。她带来一篮火红的果子，说是山里采的。屋里生了炭火，她坐在火边，影子被拉得很长。有人递给她一杯热水，她捧在手里，却没有喝，只是看着热气慢慢升起来。她叫履霜——是踩在冬天边缘的人，也是带来温暖的人。",
    flavor: "霜降之后，万物收敛，唯有这杯茶反其道而行，把夏天和秋天的甜都藏进了叶底。入口是蜜香，像蜂蜜在温水中缓缓化开；随之而来的是薯香，是炭火煨过的暖意。茶汤不薄，有冬日该有的厚实感；回甘不急不慢，像雪地里远行归来，家人递上的那杯热茶。",
    value: "冬天喝它，是应季；存着它，是存一份暖。红茶性温，不似绿茶那般急切地要与时间赛跑。三五年后，蜜香会更沉，茶汤会更醇，像是把每一个冬天都熬成了温润。",
    rank: "冬日围炉，人间值得。",
    quote: "「莫听穿林打叶声，何妨吟啸且徐行」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-89.png?sign=1780650425-703cc4a908-0-0f4c421777f1e5c6d2ca1ddef597287f35620044457b3c04ef4fd57a3aaf0907",
    quoteImage: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-96.png?sign=1780650425-97add564ed-0-3d1e3a62857efe1c938244b9ef5c3b9dd906fcfdc65c6e1e2d26a7de92c9066f"
  },
  {
    name: "漱雪",
    fullName: "漱雪 茉莉绿茶 ·冬·",
    story: "大雪封山之后，另一个女子出现了。她喜欢在雪地里走，留下一串浅浅的脚印。她走到梅树下，仰头看枝头的积雪。风吹过，雪落了她一身，她也不拂，只是站在那里，像是自己也成了一株梅。她叫漱雪——南方有雪不易。",
    flavor: "七窨一提，是七次花与茶的相遇。冲泡时，茶与花在杯中重逢，茉莉香气扑鼻而来，像大雪天里推开一扇门，满院茉莉正开——这当然是假的，茉莉冬天不开。但你的鼻子不会骗你，那香气就是夏天的、盛放的、毫无保留的。茶汤入口，绿茶的鲜爽兜底，茉莉的花香居中，一口下去，冬夏同杯。",
    value: "茉莉茶要鲜，说的不是保质期，是赏味期。花香最盛时窨制，那一点夏日便封存在了茶中。入冬后启封，以滚水冲开，窗外是雪，杯中是夏——这大概是冬天最浪漫的事。",
    rank: "一捧雪花，一夏茉莉，值一个冬天。",
    quote: "「此时无声胜有声，别有幽愁暗恨生」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-99.png?sign=1780650425-1f4d2049e7-0-039a0187f834bee4ec9569c260e63259673ce3017b101781647c04f076083247",
    quoteImage: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-106.png?sign=1780650425-d4ae0966cd-0-a2f76355efe27d8decb1922ad7cc8094d84993f1c48b43fed9c35d1af88d3a21"
  },
  {
    name: "漱月",
    fullName: "漱月 茉莉红茶 ·冬·",
    story: "月圆那夜，有人在溪边掬水。水里有月亮的倒影，她掬起来，月亮就碎了；再掬，又圆了。她一遍一遍地掬，像是在玩一个永远不会腻的游戏。她的影子落在水面上，和月亮混在一起，分不清哪个是她，哪个是月。她叫漱月——是用溪水洗月亮的人。",
    flavor: "月下窨花，红茶为底。这不是寻常的花茶，是月光与花香的相遇。红茶的醇厚托住茉莉的清灵，一杯之中，有月色的温柔，也有花的馥郁。入口，茉莉先行，清雅如溪；红茶在后，温润如月。回甘处，是花是茶，已分不清。",
    value: "月光年年有，但这款茉莉红茶是限量的。这一夜的月、这一季的花、这一刻窨制的茶，错过了便不再来。若你爱过，便存下这一盏，留给往后的某个月圆之夜。",
    rank: "月圆花好，一盏正好。",
    quote: "「掬水月在手，弄花香满衣」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-108.png?sign=1780650426-4479dd3c82-0-d74f6c8e06547c4d3919295f11db89ca91f8a28445db70f14cb12c745db2f5aa",
    quoteImage: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-115.png?sign=1780650426-7a37cc85e3-0-03d0f9c0823b16ed4d285043fdef8771785f6636065289122999588da58892b8"
  },
  {
    name: "莫离",
    fullName: "莫离 茉莉银针 ·四时·",
    story: "这些人来来去去，但总有一个人一直在。她住在山脚下那间小屋，屋前种着茉莉。花开的时候，满院子都是白的。她采花，晾花，然后把花收进瓷罐里，一层一层地铺好。有人问她为什么总是不离开，她指了指那罐花，又指了指自己。她叫莫离——花与人，都不分离。",
    flavor: "银针是骨，茉莉是魂。银针的毫香沉稳如山，茉莉的香气轻盈如风，一杯之中，风与山相遇。入口，毫香托底，是白茶的底色；茉莉在后，是花香的高潮。这杯茶没有太多复杂的变化，它胜在一个\"合\"字——骨与魂合一，花与茶不离。",
    value: "不离不弃，是这杯茶的名字，也是它的命运。银针可以老，老了更醇；茉莉不能等，等久花香散。但当它们合在一起，便是另一种永恒——不是时间的永恒，是彼此成就的永恒。存它，存的是一份\"在一起\"的信念。",
    rank: "莫离，是最好的待客之道。",
    quote: "「执子之手，与子偕老」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-117.png?sign=1780650426-30445e9887-0-250aea066a27bcd82c9d41790ed92563f662d9b22e45daad9850aaabbc35329e",
    quoteImage: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-124.png?sign=1780650426-5ea705a14a-0-a2c2bd2f83d4424036ac5f58bac7f7872d647f3e21e851448ea2334be65d3162"
  },
  {
    name: "半见",
    fullName: "半见 陈皮白茶 ·四时·",
    story: "她喜欢躲在帘子后面，看外面的人来人往。不是害羞，而是觉得，保持一点距离刚刚好。太近了会腻，太远了会淡。她叫自己半见——半藏半显，半开半合。她养了条法斗，取名若隐。若隐若隐，若有若无，是她喜欢的状态，也是她与这个世界相处的方式。",
    flavor: "陈皮与白茶，一燥一润，一动一静。陈皮的果香是跳脱的，带着新会的阳光和海风；白茶的甘醇是沉稳的，像是政和深山的静默。当它们相遇，不是谁征服谁，而是在杯中跳一支慢舞——你进我退，我柔你刚，最后融为一体，是\"半见\"最好的注脚：若隐若现，不偏不倚。",
    value: "新会陈皮，越老越值钱；政和白茶，越老越醇厚。当两者都老了，会变成什么？这是时间才有的答案。存一饼半见，偶尔打开闻一闻——陈皮的果香会越来越沉，白茶的甘甜会越来越厚，它们会老成彼此最喜欢的样子。",
    rank: "半见半藏，一半新会，一半政和。",
    quote: "「犹抱琵琶半遮面，欲说还休」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-126.png?sign=1780650426-7a9ae12a51-0-734ab547f09a9fa4bd6dd710c4f9adef61e94b7b53972d7b80dc9adee23b2b3e",
    quoteImage: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-133.png?sign=1780650426-2e9b242d7a-0-aa7e42989be7c0d660cc81f51aa4dd40e75f256c10ce0a59f6e18b8553feef54"
  },
  {
    name: "步止",
    fullName: "步止 12年白茶饼 ·传说·",
    story: "他走了很远很远的路，终于在这座山前停下来。不是走不动了，而是觉得，这里就是他要找的地方。他没有名字，来时无名，去时也无名。偶尔有人问他从哪里来，他只是指一指身后的云。有人问他叫什么，他说叫步止——不是止步不前，而是知道该在哪里停下来。他养了一条德国牧羊犬，取名守望。守望守望，守在这里，等那些走累了的旅人。",
    flavor: "十二年，是什么概念？是一棵树从幼苗长成能遮荫的绿荫，是一个孩子从出生到长成少年。十二年的白茶，也有了自己的模样：枣香是它沧桑后的温柔，药香是它来处的记忆。茶汤入口，不再是当年新茶的清鲜，而是被岁月酿过的厚与醇。一杯下去，像读了一封旧信——字迹已旧，情意却新。",
    value: "它已经等了你十二年。也许还会再等，但不必太急。十二年的白茶，滋味已近圆满；再放下去，是另一种圆满的开始。启封那天，不必急，慢慢喝，让十二年的光阴在杯中缓缓化开。",
    rank: "十二年光阴，一饼收藏。",
    quote: "「行到水穷处，坐看云起时」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-135.png?sign=1780650426-dc1360c77e-0-a5bcc1f977d033c88658a9d08e440d3556b25e420c68613ba99f362b6042f97f",
    quoteImage: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-142.png?sign=1780650426-3660681f3c-0-8a55f757862fc550c1c6f2c8c0f966c86fe807124dfbfb0c5fff66cd4f60d5e8"
  },
  {
    name: "无羁",
    fullName: "无羁 17年白茶饼 ·传说·",
    story: "他骑马走过很多地方，见识过很多风景，但他从不在任何一个地方停留太久。不是无情，而是怕情深。他觉得自己像一阵风，吹过就算了，不该留下什么。但有一年，他来到南山，遇到一条灵缇。灵缇追上了他，用鼻子蹭了蹭他的手背。他停了下来，这一停，就是很多年。他给灵缇取名无拘——无拘无束，随遇而安。无拘跟着他，他也跟着无拘。",
    flavor: "2017年，那一年发生了什么？也许你还记得，也许已经模糊。但这杯茶记得——它把那一年的阳光、雨露、山风都存了下来，变成了今天的枣香与陈香。入口，是温润的，不急不躁，像是所有棱角都已被岁月磨平。回甘悠长，是它还来不及说出口的话。",
    value: "无羁，是不被束缚。但这款茶，其实一直在等你。它自由地陈化了这些年，终于等到一个懂它的人。启封后，慢慢喝，不必追，不必赶——九年的光阴，够你喝很久很久。",
    rank: "七年陈化，无羁可期。",
    quote: "「海阔凭鱼跃，天高任鸟飞」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-145.png?sign=1780650426-8bfa54daed-0-29278e62e0f45f70a5f11ff193eadc128e5b07e195670d84903b029a897d270f",
    quoteImage: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-153.png?sign=1780650426-b1cb850bbd-0-5bfa21fc2cab0d082e8c9cce1a60c7efba40f687738136d460ade1466a73863"
  },
  {
    name: "南山",
    fullName: "南山 马年茶饼 ·传说·",
    story: "这座山没有名字，山里的人就叫它南山。后来，有个孩子出生在山下，属马那年家里做了批茶饼，有人问这茶叫什么，他说叫马年茶。后来这孩子长大了，成了山里的守护者。人们不知道他的名字，只叫他南山——山不需要名字，山就是山。他养了条藏獒，取名厚重。厚重厚重，沉稳厚重，是山的气质，也是他的。",
    flavor: "马年，是十二年一轮的轮回。2012年的那批茶，采自马年，陈于南山，如今已逾十年。十年前你也许还是个少年，也许刚学会喝茶，也许还不知道什么叫\"值得收藏\"。但那棵茶树知道，那座山知道——它们把光阴酿成了一盏茶，汤色已深，陈香已沉，木质香隐隐透出，像一位老友，不必多言，对坐便好。",
    value: "南山已老，茶亦老；南山仍在，茶常新。这是你能留给后人的东西。不是价值连城，是光阴无价。当下一代人打开这饼茶，他们喝到的不只是白茶，还有一段被完整封存的时间。",
    rank: "南山可移，此饼难再。",
    quote: "「山不在高，有仙则名；水不在深，有龙则灵」",
    image: "https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-155.png?sign=1780650426-285b333077-0-737ce1ae9c9dc03ef83d179dcf1c1f6fa9f7f2d9c6faf409f6835358369f74bb",
    quoteImage: null
  }
];

// 创建章节标题样式的辅助函数
function createTitle(title) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 200, after: 200 },
    children: [new TextRun({ text: title, bold: true, size: 32 })]
  });
}

// 创建副标题样式的辅助函数
function createSubtitle(subtitle) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 100, after: 100 },
    children: [new TextRun({ text: subtitle, size: 24 })]
  });
}

// 创建普通文本段落
function createParagraph(text, center = false) {
  return new Paragraph({
    alignment: center ? AlignmentType.CENTER : AlignmentType.LEFT,
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text: text, size: 22 })]
  });
}

// 创建标签段落（如"风味笔记"、"藏养"、"品第"）
function createLabel(label) {
  return new Paragraph({
    spacing: { before: 160, after: 80 },
    children: [new TextRun({ text: label, bold: true, size: 24 })]
  });
}

// 创建签文诗句
function createQuote(quote) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 160, after: 160 },
    children: [new TextRun({ text: quote, size: 26, italics: true })]
  });
}

// 创建分页符
function createPageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

// 创建分隔图片段落（带链接）
function createImageParagraph(imageUrl) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 100, after: 100 },
    children: [
      new TextRun({ 
        text: `[图片: ${imageUrl}]`,
        size: 18,
        color: "888888"
      })
    ]
  });
}

// 创建签文表格
function createQuoteTable() {
  const quotes = [
    ["童濛", "「溪声便是广长舌，山色无非清净身」", "浮岚", "「山色空蒙雨亦奇，水光潋滟晴方好」"],
    ["不器", "「万物静观皆自得，四时佳兴与人同」", "丹桂", "「何当共剪西窗烛，却话巴山夜雨时」"],
    ["桂兰", "「路遥知马力，日久见人心」", "听枞", "「此时无声胜有声，别有幽愁暗恨生」"],
    ["天香", "「天生我材必有用，千金散尽还复来」", "履霜", "「莫听穿林打叶声，何妨吟啸且徐行」"],
    ["漱雪", "「此时无声胜有声，别有幽愁暗恨生」", "漱月", "「掬水月在手，弄花香满衣」"],
    ["莫离", "「执子之手，与子偕老」", "半见", "「犹抱琵琶半遮面，欲说还休」"],
    ["步止", "「行到水穷处，坐看云起时」", "无羁", "「海阔凭鱼跃，天高任鸟飞」"],
    ["南山", "「山不在高，有仙则名；水不在深，有龙则灵」", "", ""]
  ];
  
  const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
  const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };
  
  const rows = quotes.map(row => {
    return new TableRow({
      children: row.map((cell, idx) => {
        if (idx === 0 || idx === 2) {
          // 茶名单元格
          return new TableCell({
            borders: cellBorders,
            width: { size: 2000, type: WidthType.DXA },
            children: [new Paragraph({ 
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ text: cell, bold: true, size: 20 })]
            })]
          });
        } else {
          // 诗句单元格
          return new TableCell({
            borders: cellBorders,
            width: { size: 5500, type: WidthType.DXA },
            children: [new Paragraph({ 
              alignment: AlignmentType.LEFT,
              children: [new TextRun({ text: cell, size: 20 })]
            })]
          });
        }
      })
    });
  });
  
  return new Table({
    columnWidths: [2000, 5500, 2000, 5500],
    rows: rows
  });
}

// 构建文档内容
const children = [];

// === 封面 ===
children.push(createTitle("南山帖"));
children.push(createSubtitle("政和·白茶"));
children.push(createSubtitle("四季十二客·三传说"));

// 封面图片
children.push(createImageParagraph("https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-3.png?sign=1780650425-05699d8bd1-0-5cec1b874869595b07aea2fb0f73c1cf4e307f3e2951e9d13ba682e37dab6db1"));

// 开篇引言诗
children.push(createParagraph("南"));
children.push(createParagraph("南山有四季，四季有十二客。"));
children.push(createParagraph("每一位山客，都是一盏茶的故事。"));
children.push(createParagraph("政和山间，雾起雾落，"));
children.push(createParagraph("茶人守着老手艺，"));
children.push(createParagraph("等一片叶子慢慢变老。"));
children.push(createParagraph("这帖，写给山，写给茶，写给品茶的人。"));

// === 春·夏 页面 ===
children.push(createPageBreak());
children.push(createTitle("春 · 夏"));
children.push(createParagraph("童濛 | 白毫银针 | 「春」  浮岚 | 福建高山绿茶 | 「春」  不器 | 白牡丹 | 「夏」"));
children.push(createImageParagraph("https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-13.png?sign=1780650425-86dacd4560-0-4e8b24b2f7360db9ea53e24aa007033ece9abf619cc502ea49523c7680e405fe"));

// === 秋·冬 页面 ===
children.push(createPageBreak());
children.push(createTitle("秋 · 冬"));
children.push(createParagraph("丹桂 | 桂花红茶 | 「秋」  桂兰 | 肉桂 | 「秋」  听枞 | 老枞 | 「秋」  天香 | 大红袍 | 「秋」"));
children.push(createParagraph("履霜 | 工夫红茶 | 「冬」  漱雪 | 茉莉绿茶 | 「冬」  漱月 | 茉莉红茶 | 「冬」"));
children.push(createImageParagraph("https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-16.png?sign=1780650425-3d0ce42bf4-0-2c3665b81a9eafe20d9a4da712395852fdf5d65f1220c12aae25b87b1f237089"));

// === 四时·传说 页面 ===
children.push(createPageBreak());
children.push(createTitle("四时 · 传说"));
children.push(createParagraph("莫离 | 茉莉银针 | 「四时」  半见 | 陈皮白茶 | 「四时」  步止 | 白茶饼 | 「传说」  无羁 | 17年白茶饼 | 「传说」  南山 | 马年茶饼 | 「传说」"));
children.push(createImageParagraph("https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-19.png?sign=1780650425-59f973c17c-0-f4fede15a12ad936dba82a278c36a6ba838bdbecda84697a7d703c8bd0a22d1c"));
children.push(createImageParagraph("https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-20.png?sign=1780650425-e3c1861341-0-9a1de71e7a44c6ddad5a1419317df4f218607e17897d0ba65d232c6a5c59f32f"));

// === 15款茶内容 ===
for (const tea of teaData) {
  children.push(createPageBreak());
  
  // 茶名标题
  children.push(createTitle(tea.fullName));
  
  // 产品图片
  children.push(createImageParagraph(tea.image));
  
  // 故事
  children.push(createParagraph(tea.story));
  
  // 风味笔记
  children.push(createLabel("风味笔记"));
  children.push(createParagraph(tea.flavor));
  
  // 藏养（原来是收藏价值）
  children.push(createLabel("藏养"));
  children.push(createParagraph(tea.value));
  
  // 品第（新增）
  children.push(createLabel("品第"));
  children.push(createParagraph(tea.rank));
  
  // 签文诗句
  children.push(createQuote(tea.quote));
  
  // 签文图片
  if (tea.quoteImage) {
    children.push(createImageParagraph(tea.quoteImage));
  }
}

// === 签文摘选表 ===
children.push(createPageBreak());
children.push(createTitle("签文 · 摘选"));
children.push(createQuoteTable());

// 签文表格后的图片
children.push(createImageParagraph("https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-164.png?sign=1780650426-d8944d0b17-0-610be07300339810f62d9b18996602bdd435f65fadaa8beb2bb08f691e290f2c"));

// === 尾页 ===
children.push(createPageBreak());
children.push(createTitle("你 是第十三位"));
children.push(createParagraph("四季十二客，山间已至"));
children.push(createParagraph("三位传说，等你结缘"));
children.push(createParagraph("每一位品茶的你，都是独一无二的山客"));

// 尾页图片1
children.push(createImageParagraph("https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-169.png?sign=1780650426-e8c411ad1d-0-95385b62f3bb517525af53d4bea37e50ab11f5c402b24244077f9bdb1d5a266e"));

children.push(createParagraph("扫码·遇见你的山客"));
children.push(createSubtitle("南山帖"));
children.push(createSubtitle("政和·白茶"));
children.push(createSubtitle("四季十二客·三传说"));

// 尾页图片2
children.push(createImageParagraph("https://static.coze.site/7635688502080078121-data_volume/generated/20260506/660ef019-dccd-4954-80bf-a30fdd31a8dd/id-174.png?sign=1780650426-0639c45089-0-cc6935542489e86bebd1c78f1d96ef5a18161c93fcc9847e316096940adaad88"));

// 创建文档
const doc = new Document({
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: children
  }]
});

// 导出为文件
const outputPath = "/app/data/所有对话/主对话/白茶品牌/南山帖_品牌手册_修订版V2.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
  console.log("文档已成功创建: " + outputPath);
});
