from util.encryption import Encryption
from util.util import gen_prime
from util.elliptic_curves import ECurve, ECPoint, str_to_point
import random
import math

class ElGamalEC(Encryption):
    def __init__(self, k: int = 1000, public_keys: tuple = None, priv_key: int = None, num_checks: int = 100):
        if not public_keys:
            self.q = gen_prime(k, num_checks=num_checks)
            self.a, self.b = self.get_ab()
            self.curve = ECurve(self.a, self.b, self.q)
            self.g = self.get_generator()

            self.n = random.randint(1, 10) # TODO: this is awful, this needs to be redone
            self.p = self.n * self.g
        else:
            self.q, self.a, self.b, self.g, self.p = public_keys

            self.curve = ECurve(self.a, self.b, self.q)
            self.g = str_to_point(self.g, self.curve, comma=True)
            self.p = str_to_point(self.p, self.curve, comma=True)

            self.n = priv_key if priv_key else random.randint(1, 10)

        self.k = math.floor(math.log2(self.q))

    @property
    def pub_keys(self):
        return self.q, self.a, self.b, self.g, self.p

    @property
    def private_key(self):
        return self.n

    def get_ab(self):
        try:
            a = random.randint(1, self.q // 2)
            b = random.randint(1, self.q // 2)
            ECurve(a, b, self.q) # this will raise a ValueError if a and b don't work
            return a, b
        except ValueError:
            return self.get_ab()

    def get_generator(self) -> ECPoint:
        for _ in range(10 * self.q):
            x = random.randint(1, self.q - 1)
            y = random.randint(1, self.q - 1)
            p = ECPoint(x, y, self.curve)
            if p.valid():
                p *= random.randint(1, self.q)
                if not p.inf:
                    return p
        raise Exception(f'Unable to find a point on {self.curve} after {10 * self.q} attempts')

    def encrypt(self, x: ECPoint) -> tuple[ECPoint, ECPoint]:
        m = random.randint(1, self.q - 1)
        alpha = m * self.g
        omega = m * self.p
        y = x + omega
        return (y, alpha)

    def decrypt(self, y: ECPoint, alpha: ECPoint) -> int:
        point = y - (self.n * alpha)
        return point.x

    def decrypt_text(self, cypher: list) -> str:
        # Parse the cypher list before actual processing
        cypher = [(ECPoint(c[0], c[1], self.curve), ECPoint(c[2], c[3], self.curve)) for c in cypher]
        return super().decrypt_text(cypher)


if __name__ == '__main__':
    # Assignment 3 test (first char)
    q = 111697039144439244274158398653562346085125490793664062732425069223685968110844126905903321206114392849452542256992315754843167574112467024858088205347572299296687223643952822745811271693456632679803618511515217807199664219990752590959138703164100104061985978987701427311881250925416668035932094333108552446839
    a = 150670258656281464005027759708221023233910114637886003539106738481215882957713483236742237072518545883429463829128035822122070539009268529588117340272238455156286895193960706935802180341819752120102766312902122204702353872155278694417075931419847141024333493817900461006527055261695842425790546228916431325513
    b = 104815861020657080241596578752393940140617569980803135496881290764938288013364134928068097698824115341484980977151298278192209798477977140363086488236483224661104202521225088803004668319349969513561776896401494842782206897897856458042025648888304723359320219472250799841670786377536581380629352855788742594142

    curve = ECurve(a, b, q)
    g = ECPoint(61643059794514658855856979240384380792004005595902002474204661739186732752684754456411382735922901235495907950404348644170841371014778432355106487961684475960234463142352681608311501007071362596770681949544839546671743458092267656460600660256785359231219517003730759173037578221710970121586110683785072217662,
                54359302960000760545008891946403739583148786728166654515466055048776801978921702648886655754375020415206500780463313877521057493281570465893562576850601434219889617981357296583120996241733031701559848144381511290881538520012299210485219015267103348638818685963120393173867173336217274772249726418109868176493,
                curve)
    p = ECPoint(60949449667193749252503359889850425121315508973346945821886368823756771832998966289937779780434994149115196710111811694044123631896909518754733352427887648092521748310305738624343577584577041608478447076368817057789725108338375345629371222211045251384720803595793058052264980931562187712908832419030905731456,
                61732224616283043648568020304215677416953487728868336147524271976573117696218390316816254546008953094848938572310947651922118368895678399666836335369620907736296238282509607980572392998672197795698218685116119057168223625468009549912498255285830874111241719004852772790800875392292105908437344598596511413453,
                curve)

    el = ElGamalEC(public_keys=(q, a, b, g, p), n=3)

    with open('a3.cipher.txt', 'r') as f:
        lines = f.readlines()

    line = lines[0]
    parts = [int(p) for p in line.split(' ')]
    c = ECPoint(parts[0], parts[1], curve)
    h = ECPoint(parts[2], parts[3], curve)

    char = el.decrypt(c, h)
    print(char, chr(char))
    assert char == 97
