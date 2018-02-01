# coding: utf-8

def tripTime(trip1):

        if type(trip1) == list:
            hr1, mn1 = trip1[0].get("Origin").get("time").split(":")
            hr2, mn2 = trip1[-1].get("Destination").get("time").split(":")
            hr1, hr2, mn1, mn2 = int(hr1), int(hr2), int(mn1), int(mn2)
            if not trip1[0].get("Origin").get("date") == trip1[-1].get("Destination").get("date"):
                if hr1 < hr2:
                    hr1 += 24
                else:
                    hr2 += 24
        else:
            hr1, mn1 = trip1.get("Origin").get("time").split(":")
            hr2, mn2 = trip1.get("Destination").get("time").split(":")
            hr1, hr2, mn1, mn2 = int(hr1), int(hr2), int(mn1), int(mn2)
            if not trip1.get("Origin").get("date") == trip1.get("Destination").get("date"):
                if hr1 < hr2:
                    hr1 += 24
                else:
                    hr2 += 24
        mn1 += hr1 * 60
        mn2 += hr2 * 60
        tTime = mn2 - mn1
        tH = tTime // 60
        tM = tTime % 60
        return tTime, tH, tM