Rulebook.ages = (function() {
    flaw1 = ['agility', 'athletics', 'endurance'];
    flaw2 = ['agility', 'athletics', 'awareness', 'cunning', 'endurance', 'fighting', 'marksmanship'];

    return [
        {
            name: 'youth',
            min: 0,
            max: 9,
            skillCap: 4,
            experience: 120,
            specialty: 40,
            destiny: 7,
            benefitCap: 3,
            drawback: false,
            flaws: 0
        },
        {
            name: 'adolecent',
            min: 10,
            max: 13,
            experience: 150,
            skillCap: 4,
            specialty: 40,
            destiny: 6,
            benefitCap: 3,
            drawback: false,
            flaws: 0
        },
        {
            name: 'young adult',
            min: 14,
            max: 18,
            skillCap: 5,
            experience: 180,
            specialty: 60,
            destiny: 5,
            benefitCap: 3,
            drawback: false,
            flaws: 0
        },
        {
            name: 'adult',
            min: 18,
            max: 30,
            skillCap: 7,
            experience: 210,
            specialty: 80,
            destiny: 4,
            benefitCap: 3,
            drawback: true,
            flaws: 0
        },
        {
            name: 'middle age',
            min: 30,
            max: 50,
            skillCap: 6,
            experience: 240,
            specialty: 100,
            destiny: 3,
            benefitCap: 3,
            drawback: false,
            flaws: 1,
            flawed: flaw1
        },
        {
            name: 'old',
            min: 50,
            max: 70,
            skillCap: 5,
            experience: 270,
            specialty: 160,
            destiny: 2,
            benefitCap: 2,
            drawback: true,
            flaws: 1,
            flawed: flaw2
        },
        {
            name: 'very old',
            min: 70,
            max: 80,
            skillCap: 5,
            experience: 330,
            specialty: 200,
            destiny: 1,
            benefitCap: 1,
            drawback: true,
            flaws: 2,
            flawed: flaw2
        },
        {
            name: 'venerable',
            min: 80,
            max: null,
            skillCap: 5,
            experience: 360,
            specialty: 240,
            destiny: 0,
            benefitCap: 0,
            drawbacks: 1,
            drawback: true,
            flaws: 3,
            flawed: flaw2
        }
    ];
})();
