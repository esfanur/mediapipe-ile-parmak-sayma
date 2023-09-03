import cv2
import mediapipe as mp
import handlmarksmodul as hmm
import pyttsx3 # Metinden konuşmaya dönüştürme için bir kütüphane.

cam=cv2.VideoCapture(0)
decetor=hmm.HandLandmarks(mindetecconf=0.8) #Minimum algılama güvenliği eşiği 0.8 olan bir el işareti algılayıcı oluşturur
encodin=pyttsx3.init() #Metinden konuşma motorunu başlat
lnmkrnok=[4,8,12,16,20] #Belirli parmaklar için işaret noktalarının endekslerini içeren bir liste olusturduk bu noktaların denk geldıgı parmaklar(başparmak, işaret parmağı, orta parmak, yüzük parmağı, serçe parmağı)
totalfin=0 #Algılanan parmakların toplam sayısını takip etmek için bir değişken.
while True:
    _,frame=cam.read()
    decetor.findhand(frame) #El işareti algılayıcısını mevcut karedeki elleri bulmak için
    lmlist=decetor.handfindpos(frame,draw=False)

    if len(lmlist)!=0: #Eğer el işaretleri algılanırsa
        fingers=[] #Her parmağın durumunu temsil etmek için boş bir liste (fingers)'ı olsuturdurk

        if lmlist[lnmkrnok[0]][1] > lmlist[lnmkrnok[0] - 1][1]: #Bu kod, sadece başparmağın durumunu kontrol eder
                fingers.append(1)
                #print("sag el")
        else:
            fingers.append(0)
        for id in range(1,5):
            if lmlist[lnmkrnok[id]][2]<lmlist[lnmkrnok[id]-2][2]:
                fingers.append(1)
                #print("parmak acık")
                """
                işaret parmağı, orta parmak, yüzük parmağı ve serçe parmağı için her birini ayrı ayrı kontrol eder,
                her bir parmağın açık (yukarı kaldırılmış) mı yoksa kapalı (aşağı indirilmiş) mı olduğunu belirler.
                her bir parmağın açık veya kapalı olup olmadığını tespit eder ve bu bilgileri fingers listesine ekler
                """

            else:
                fingers.append(0)
        # print(fingers)
        totalfin=fingers.count(1) #Kaldırılan parmakları sayın ve bunu totalfin içinde saklayın.
        print(totalfin)

    cv2.rectangle(frame,(10,10),(200,200),(185,178,168),-1)
    cv2.putText(frame,str(totalfin),(70,130),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,0),8)
    encodin.say(totalfin)
    encodin.runAndWait()
    cv2.imshow("kamera",frame)

    if cv2.waitKey(1)==ord("q"):
        break

cam.release()
cv2.destroyAllWindows()