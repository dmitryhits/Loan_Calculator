import math
import argparse

# loan_principal = 'Loan principal: 1000'
# final_output = 'The loan has been repaid!'
# first_month = 'Month 1: repaid 250'
# second_month = 'Month 2: repaid 250'
# third_month = 'Month 3: repaid 500'
#
# # write your code here
# print(loan_principal)
# print(first_month)
# print(second_month)
# print(third_month)
# print(final_output)


class Credit:
    def __init__(self):
        # self.request = input("""What do you want to calculate?
        # type "n" for number of monthly payments,
        # type "a" for annuity monthly payment amount,
        # type "p" for loan principal:
        # """)
        self.principal = -1
        self.length = -1
        self.payments = -1
        self.interest = -1

    def set_principal(self, principal):
        self.principal = principal
        # self.principal = float(input('Enter the loan principal:\n'))

    def set_interest(self, interest):
        self.interest = interest / 1200
        # self.interest = float(input('Enter the loan interest:\n')) / 1200

    def set_length(self, number_of_months):
        self.length = number_of_months
        # self.length = int(input('Enter the number of periods:'))

    def set_payments(self, annuity_payment):
        self.payments = annuity_payment
        # self.payments = float(input('Enter the annuity payment:\n'))

    def calc_months(self):
        monthly_payment = int(input('Enter the monthly payment:\n'))
        months = math.ceil(self.principal / monthly_payment)
        print(f'It will take {months} month{"" if months == 1 else "s"} to repay the loan')

    def calc_differentiated_payments(self, principal, interest, number_of_months, payment_number):
        self.set_principal(principal)
        self.set_length(number_of_months)
        self.set_interest(interest)
        principal_payment = self.principal / self.length
        interest_payment = self.interest * (self.principal - self.principal * (payment_number - 1) / self.length)
        payment = math.ceil(principal_payment + interest_payment)

        print(f'Month {payment_number}: payment is {payment}')
        return payment

    def calc_length(self, principal, annuity_payment, interest):
        self.set_principal(principal)
        self.set_payments(annuity_payment)
        self.set_interest(interest)
        length = math.log(self.payments / (self.payments - self.interest * self.principal), 1 + self.interest)
        length = math.ceil(length)
        years = length // 12
        months = length % 12
        over_payment = length * annuity_payment - principal
        if years == 0:
            print(f'It will take {months} month{"" if months == 1 else "s"} to repay this loan!')
        elif months == 0:
            print(f'It will take {years} year{"" if years == 1 else "s"} to repay this loan!')
        else:
            print(f'It will take {years} year{"" if years == 1 else "s"} '
                  f'and {months} month{"" if months == 1 else "s"} to repay this loan!')
        print(f'Overpayment = {over_payment}')

    def calc_annuity(self, principal, number_of_months, interest):
        self.set_principal(principal)
        self.set_length(number_of_months)
        self.set_interest(interest)
        # print(self.principal, self.length, self.interest)
        monthly_payment = self.principal * self.interest * math.pow(1 + self.interest, self.length) \
            / (math.pow(1 + self.interest, self.length) - 1)
        print(f'Your monthly payment = {math.ceil(monthly_payment)}!')
        over_payment = math.ceil(monthly_payment) * number_of_months - principal
        print(f'Overpayment = {over_payment}')

    def calc_principal(self, annuity_payment, number_of_month, interest):
        self.set_payments(annuity_payment)
        self.set_length(number_of_month)
        self.set_interest(interest)
        principal = self.payments * (math.pow(1 + self.interest, self.length) - 1) \
            / (self.interest * math.pow(1 + self.interest, self.length))
        print(f'Your loan principal = {round(principal)}!')
        over_payment = annuity_payment * number_of_month - principal
        print(f'Overpayment = {over_payment}')

    def calc_payments(self):
        months = int(input('Enter the number of months:\n'))
        remainder = self.principal % months
        if remainder == 0:
            print(f'Your monthly payment = {self.principal // months}')
        else:
            monthly = math.ceil(self.principal / months)
            last = self.principal - monthly * (months - 1)
            print(f'Your monthly payment = {monthly} and the last payment = {last}.')

parser = argparse.ArgumentParser()
parser.add_argument('--type', choices=['diff', 'annuity'])
parser.add_argument('--payment')
parser.add_argument('--principal')
parser.add_argument('--periods')
parser.add_argument('--interest')
args = parser.parse_args()

loanshark = Credit()
# print(vars(args))
var = [v for v in vars(args).values() if v]
if not args.interest or len(var) < 4 or not args.type:
    print('Incorrect parameters')
else:
    if args.type == "annuity":
        if args.principal and args.periods and args.interest:
            loanshark.calc_annuity(float(args.principal), int(args.periods), float(args.interest))
        elif args.payment and args.periods and args.interest:
            loanshark.calc_principal(float(args.payment), int(args.periods), float(args.interest))
        elif args.principal and args.payment and args.interest:
            loanshark.calc_length(float(args.principal), float(args.payment), float(args.interest))
        else:
            print('Incorrect parameters')
    elif args.type == "diff":
        if args.payment:
            print('Incorrect parameters')
        else:
            total = 0
            for i in range(1, int(args.periods) + 1):
                total += loanshark.calc_differentiated_payments(float(args.principal), float(args.interest),
                                                       int(args.periods), i)
            print(f'Overpayment = {total - float(args.principal)}')
    else:
        print('Incorrect parameters')
