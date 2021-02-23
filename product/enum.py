
LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
    ('X', 'default'),
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
    ('D', 'Delivery'),
    ('X', 'Default'),
)

GENDER_CHOICES = (
    ('H', 'Homme'),
    ('F', 'Femme'),
    ('E', 'Enfant'),
    ('X', 'Default'),
)

COLOR_CHOICES = (
    ('B', 'Black'),
    ('W', 'White'),
    ('R', 'Red'),
    ('X', 'Default'),
)

CLOTH_SIZE_CHOICES = (
    ('L', 'Large'),
    ('M', 'Medium'),
    ('S', 'Small'),
    ('X', 'Default'),
)

SHOES_SIZE_CHOICES = (
    ('32', 'Adulte'),
    ('20', 'Enfant'),
    ('45', 'Adulte2'),
    ('X', 'Default'),
)

STATUS_CHOICES = (
    ('D', 'Draft'),
    ('P', 'Published'),
    ('X', 'Delete')
)

ORIGIN = (
    ('L', 'Locale'),
    ('I', 'Internationale'),
    ('X', 'Default')
)


TOWN = (
    ('X', 'Default'),
    ('1', 'DAKAR'),
    ('9', 'Dakar Plateau'),
    ('2', 'Dakar Plateau GUEULE TAPEE'),
    ('3', 'Dakar Plateau FASS'),
    ('4', 'Dakar Plateau COLOBANE'),
    ('5', 'Dakar Plateau POINT E'),
    ('6', 'Dakar Plateau AMITIE'),
    ('7', 'Dakar Plateau GOREE'),
    ('8', 'Dakar Plateau MEDINA'),
    ('10', 'Parcelles Assainies'),
    ('11', 'Parcelles Assainies Grand YOFF'),
    ('12', 'Parcelles Assainies PATTE D OIE'),
    ('13', 'Parcelles Assainies CAMBERENE'),
    ('14', 'Grand Dakar'),
    ('15', 'Grand Dakar BISCUITERIE'),
    ('16', 'Grand Dakar HLM'),
    ('17', 'Grand Dakar HANN BEL AIR'),
    ('18', 'Grand Dakar DIEUPPEUL DERKLE'),
    ('19', 'Grand Dakar SICAP LIBERTE'),
    ('20', 'Almadies'),
    ('21', 'Almadies YOFF'),
    ('22', 'Almadies MERMOZ SACRE COEUR'),
    ('23', 'Almadies NGOR'),
    ('24', 'Almadies OUAKAM'),
    ('25', 'Guédiawaye'),
    ('26', 'Guédiawaye GOLF SUD'),
    ('27', 'Guédiawaye MEDINA GOUNASS'),
    ('28', 'Guédiawaye NDIAREME'),
    ('29', 'Guédiawaye SAM NOTAIRE'),
    ('30', 'Guédiawaye WAKHINANE NIMZAT'),
    ('31', 'Pikine'),
    ('32', 'Pikine Dagoudane DALIFORT'),
    ('33', 'Pikine Dagoudane DJIDA THIAROYE KAO'),
    ('34', 'Pikine Dagoudane GUINAW RAIL NORD'),
    ('35', 'Pikine Dagoudane GUINAW RAIL SUD'),
    ('36', 'Pikine Dagoudane EST'),
    ('37', 'Pikine Dagoudane NORD'),
    ('38', 'Pikine Dagoudane OUEST'),
    ('39', 'Niayes KEUR MASSAR'),
    ('40', 'Niayes MALIKA'),
    ('41', 'Niayes YEUMBEUL NORD'),
    ('42', 'Niayes YEUMBEUL SUD'),
    ('43', 'Thiaroye MBAO'),
    ('44', 'Thiaroye SICAP MBAO'),
    ('45', 'THIAROYE GARE'),
    ('46', 'THIAROYE SUR MER'),
    ('47', 'THIAROYE TIVAVOUANE DIAKSAO'),
    ('48', 'Thiaroye DIAMAGUENE'),
    ('49', 'RUFISQUE EST'),
    ('50', 'RUFISQUE NORD'),
    ('51', 'RUFISQUE OUEST'),
    ('52', 'LIBERTE 1'),
    ('53', 'LIBERTE 2'),
    ('54', 'LIBERTE 3'),
    ('55', 'LIBERTE 4'),
    ('56', 'LIBERTE 5'),
    ('57', 'LIBERTE 6'),
    ('58', 'SACREE COEUR'),
    ('59', 'MAMELLE'),
    ('60', 'NORD FOIR'),
    ('61', 'OUEST FOIR'),
    ('62', 'FOIR')
)

ORDER_STATUS = (
    ('VALIDATED', 'En cours'),
    ('DELIVERED', 'Livrée'),
    ('CANCEL', 'Annulée'),
    ('DRAFT', 'En brouillon')
)
PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    # ('P', 'PayPal'),
    # ('C', 'Carte de crédit'),
    ('L', 'Livraison')
    # ('V', 'Virement bancaire'),
)
