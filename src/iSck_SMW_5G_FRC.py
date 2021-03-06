""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
SMW = iSocket().open('192.168.58.114', 5025)
cat_FR1b_60  = {'FR1A13', 'FR1A16', 'FR1A23', 'FR1A19', 'FR1A26'}
cat_FR1b_30  = {'FR1A12', 'FR1A15', 'FR1A18', 'FR1A22', 'FR1A25', 'FR1A311', 'FR1A312', 'FR1A313', 'FR1A314', 'FR1A318', 'FR1A319', 'FR1A320', 'FR1A321', 'FR1A325', 'FR1A326', 'FR1A327', 'FR1A328', 'FR1A330', 'FR1A332', 'FR1A34', 'FR1A35', 'FR1A36', 'FR1A37', 'FR1A411', 'FR1A412', 'FR1A413', 'FR1A414', 'FR1A418', 'FR1A419', 'FR1A420', 'FR1A421', 'FR1A425', 'FR1A426', 'FR1A427', 'FR1A428', 'FR1A44', 'FR1A45', 'FR1A46', 'FR1A47', 'FR1A511', 'FR1A512', 'FR1A513', 'FR1A514', 'FR1A54', 'FR1A55', 'FR1A56', 'FR1A57'}
cat_FR1a_15  = {'FR1A11', 'FR1A14', 'FR1A17', 'FR1A21', 'FR1A24', 'FR1A31', 'FR1A310', 'FR1A315', 'FR1A316', 'FR1A317', 'FR1A32', 'FR1A322', 'FR1A323', 'FR1A324', 'FR1A329', 'FR1A33', 'FR1A331', 'FR1A38', 'FR1A39', 'FR1A41', 'FR1A410', 'FR1A415', 'FR1A416', 'FR1A417', 'FR1A42', 'FR1A422', 'FR1A423', 'FR1A424', 'FR1A43', 'FR1A48', 'FR1A49', 'FR1A51', 'FR1A510', 'FR1A52', 'FR1A53', 'FR1A58', 'FR1A59'}
cat_FR1     = {'FR1A11', 'FR1A12', 'FR1A13', 'FR1A14', 'FR1A15', 'FR1A16', 'FR1A17', 'FR1A18', 'FR1A19', 'FR1A21', 'FR1A22', 'FR1A23', 'FR1A24', 'FR1A25', 'FR1A26', 'FR1A31', 'FR1A310', 'FR1A311', 'FR1A312', 'FR1A313', 'FR1A314', 'FR1A315', 'FR1A316', 'FR1A317', 'FR1A318', 'FR1A319', 'FR1A32', 'FR1A320', 'FR1A321', 'FR1A322', 'FR1A323', 'FR1A324', 'FR1A325', 'FR1A326', 'FR1A327', 'FR1A328', 'FR1A329', 'FR1A33', 'FR1A330', 'FR1A331', 'FR1A332', 'FR1A34', 'FR1A35', 'FR1A36', 'FR1A37', 'FR1A38', 'FR1A39', 'FR1A41', 'FR1A410', 'FR1A411', 'FR1A412', 'FR1A413', 'FR1A414', 'FR1A415', 'FR1A416', 'FR1A417', 'FR1A418', 'FR1A419', 'FR1A42', 'FR1A420', 'FR1A421', 'FR1A422', 'FR1A423', 'FR1A424', 'FR1A425', 'FR1A426', 'FR1A427', 'FR1A428', 'FR1A43', 'FR1A44', 'FR1A45', 'FR1A46', 'FR1A47', 'FR1A48', 'FR1A49', 'FR1A51', 'FR1A510', 'FR1A511', 'FR1A512', 'FR1A513', 'FR1A514', 'FR1A52', 'FR1A53', 'FR1A54', 'FR1A55', 'FR1A56', 'FR1A57', 'FR1A58', 'FR1A59'}

for file in cat_FR1:
    SMW.write(f'SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:TYPE {file}')
    setFile = SMW.query(f'SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:TYPE?')
    # print(f'{file}  {setFile}')
    if file == setFile:
        print(setFile)
