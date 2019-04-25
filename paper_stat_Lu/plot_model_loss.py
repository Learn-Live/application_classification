import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams.update({'figure.autolayout': True})

loss = [2.4068861772984635, 1.9946499930487738, 1.6362912825175695, 1.4837432691870123, 1.4147392887707531,
        1.3513979556489033, 1.3189882182990853, 1.3066226193513819, 1.3017109792278767, 1.2927164558380368,
        1.289290674149044, 1.2871316911051514, 1.2849301463502214, 1.2819311282411874, 1.2803080636988242,
        1.2801234415178786, 1.2799548112526142, 1.27827963564131, 1.2775305328755993, 1.2781436611525385,
        1.2757071159924569, 1.2770045249340185, 1.2746394658214832, 1.2760239917344727, 1.2741469510648615,
        1.275181992764616, 1.2732781834072537, 1.2724605043939392, 1.2725421047294792, 1.272013462620017,
        1.2729327994048911, 1.2714106117817039, 1.2729570327402213, 1.2714401969203242, 1.2712780762812028,
        1.2719822926496072, 1.2708152208799197, 1.2696430113370245, 1.26972833722567, 1.2710658141544886,
        1.2702408558056679, 1.2690275497537442, 1.2685404086659615, 1.2699177317728652, 1.268736793881371,
        1.2694653640558691, 1.2703077330580885, 1.2678811117034321, 1.2699697858652319, 1.2678802665158764,
        1.2680502064013608, 1.2688902797312123, 1.2677269433961764, 1.2683178423994221, 1.2683859792335954,
        1.2667491730348563, 1.2668315029228385, 1.2672973436022561, 1.2669063465935844, 1.2657586073328788,
        1.2667515368268183, 1.2657376079962999, 1.2673187300010964, 1.2658942199888683, 1.2653051759830858,
        1.2663250228084584, 1.2675908137461076, 1.2655657418400732, 1.2657294067335718, 1.265762323845421,
        1.2647938179591345, 1.2650985793461875, 1.2657975963394057, 1.2688531137648082, 1.2653033270827467,
        1.2644675799778529, 1.2642555606848769, 1.2643601002937062, 1.2640937709724251, 1.2641699101769315,
        1.2643361261912756, 1.2638844112870555, 1.2640321309394096, 1.2640321170631961, 1.2639014725121662,
        1.2641909330610246, 1.2638292337851549, 1.2637553473629017, 1.2647927835504844, 1.2681239084381695,
        1.2647310335589885, 1.2650453615440893, 1.2641341169044453, 1.2642126472328497, 1.2644994210524114,
        1.2640995600866893, 1.2646552547155445, 1.2640036674613886, 1.264144026833657, 1.2641362029618897]
val_loss = [2.2249909052773127, 1.7499023070411077, 1.5864084334600539, 1.5451536538108948, 1.5058397962933494,
            1.5107314000054011, 1.5260486300029452, 1.5126470421987868, 1.5179152450864277, 1.5090197835649763,
            1.5060769281690083, 1.5074371818512204, 1.5101683783152746, 1.5038896326034787, 1.495857452589368,
            1.4955944220225017, 1.4946567671639579, 1.4777399377217368, 1.4864433644309876, 1.4799163303677998,
            1.4705606320547679, 1.4777991279723153, 1.4784938418675984, 1.4815348538141402, 1.4788747496075101,
            1.4820144195405265, 1.4745992403181771, 1.4813875451920524, 1.4886240523958962, 1.4830467227905515,
            1.4782553646299574, 1.4749277470603821, 1.490398367245992, 1.4843298121104165, 1.5050237651855227,
            1.4889132106114948, 1.493309741928464, 1.4849869334508503, 1.4837685690985785, 1.4825327169327509,
            1.4782691247879514, 1.4952550766960022, 1.4991035385737344, 1.491127125800602, 1.471606663295201,
            1.5144522379315088, 1.5195890456911116, 1.5544568905754694, 1.5124250915315416, 1.5288908027467274,
            1.513176921814207, 1.5159186124801636, 1.5287335505561224, 1.510727670457628, 1.5024914325229706,
            1.5083082952196636, 1.5233174921974304, 1.5162931869900416, 1.5036533446539015, 1.4991095766188607,
            1.498808913760715, 1.5018825966214377, 1.5135987296937004, 1.5026307616915022, 1.4994424032786535,
            1.4855819032305764, 1.5110933383305867, 1.5010209802597287, 1.4737071271926638, 1.4927370396871416,
            1.4925815302228171, 1.4764029733718387, 1.4888315276494102, 1.4984197673343478, 1.4730568386259533,
            1.4667169593629383, 1.4809374922797793, 1.4701726342004442, 1.4714766930020045, 1.4799808623298767,
            1.471967241120717, 1.463430885284666, 1.4787009973374625, 1.477591385917058, 1.4738067975119939,
            1.4702585027331398, 1.4700856341256037, 1.4680379875122556, 1.4668746827140686, 1.4739546529830447,
            1.4638810933582367, 1.4406066205766466, 1.4594524228383625, 1.4538436957768031, 1.4638346868848044,
            1.4516332660402571, 1.4693883525000677, 1.4508615334828694, 1.4569413321358817, 1.4562423550893391]

plt.plot(loss, 'b-^')
plt.plot(val_loss, 'r-o')
# plt.title('Model loss')
plt.ylabel('Losses in training phase')
plt.xlabel('Epochs')
plt.legend(['Train_loss', 'Test_loss'], loc='upper right')
# plt.savefig('loss.jpg')
plt.savefig('losses_in_training_phase.pdf')
plt.show()
