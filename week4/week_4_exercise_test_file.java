public class BankAccount {
    private String owner;
    private double balance;
    private boolean isActive;

    public BankAccount(String owner, double initialDeposit) {
        if (initialDeposit < 0) {
            throw new IllegalArgumentException("Initial deposit must be non-negative");
        }
        this.owner = owner;
        this.balance = initialDeposit;
        this.isActive = true;
    }

    public void deposit(double amount) {
        if (!isActive) {
            throw new IllegalStateException("Cannot deposit to an inactive account");
        }
        if (amount <= 0) {
            throw new IllegalArgumentException("Deposit must be positive");
        }
        this.balance += amount;
    }

    public void withdraw(double amount) {
        if (!isActive) {
            throw new IllegalStateException("Cannot withdraw from an inactive account");
        }
        if (amount <= 0) {
            throw new IllegalArgumentException("Withdrawal must be positive");
        }
        if (amount > balance) {
            throw new IllegalArgumentException("Insufficient funds");
        }
        this.balance -= amount;
    }

    public double getBalance() {
        return balance;
    }

    public void closeAccount() {
        this.isActive = false;
    }

    public boolean isActive() {
        return isActive;
    }

    public String getOwner() {
        return owner;
    }
}