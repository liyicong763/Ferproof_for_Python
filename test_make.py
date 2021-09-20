import random
def make_test4():
   file_write = open('test4.txt', mode='w')
   for i in range(100):
       for ii in range(4):
          a1 = random.uniform(0, 200000)
          if i <= 8:
             a = round(a1, i)
          else:
             a = round(a1, 8)

          b1 = random.uniform(a1, 200000)
          if i <= 8:
             b = round(b1, i)
          else:
             b = round(b1, 8)
          m1 = random.uniform(a1, b1)
          if i <= 8:
             m = round(m1, i)
          else:
             m = round(m1, 8)
          file_write.writelines([str(m), " ", str(a), " ", str(b), '\n'])
   file_write.close()
def make_orgtest():
   file_write = open('org_test.txt', mode='w')
   for i in range(400):
      a = 32
      b = 0
      if i< 5:
         file_write.writelines([str(i), " ", str(4), '\n'])
      if i> 5 and i<100:
         file_write.writelines([str(i), " ", str(8), '\n'])
      if i > 100 and i < 200:
         file_write.writelines([str(i * 100), " ", str(16), '\n'])
      if i > 200 and i < 300:
         file_write.writelines([str(i * 10000000), " ", str(32), '\n'])
      if i > 300 and i < 400:
         file_write.writelines([str(i * 100000000000000), " ", str(64), '\n'])
   file_write.close()

make_orgtest()